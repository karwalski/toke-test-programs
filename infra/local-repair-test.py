#!/usr/bin/env python3
"""local-repair-test.py — Test repair loop locally on selected failed programs.

Runs the full repair pipeline (RAG + improved prompts + history chaining)
on a small set of programs to validate before deploying to workers.
"""

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import requests
import yaml

# Reuse the worker modules
sys.path.insert(0, str(Path(__file__).resolve().parent))
from toke_docs_lookup import get_context_for_repair as rag_context

BASE_DIR = Path(__file__).resolve().parent.parent
SOLUTIONS_DIR = BASE_DIR / "results" / "solutions"
CATEGORIES_DIR = BASE_DIR / "categories"

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
TKC = "tkc"
MAX_ITERATIONS = 5
TEST_TIMEOUT = 10

# Load the system and repair prompts from worker-generate.py
# (importing would require all deps, so just read them)
_worker_py = (Path(__file__).resolve().parent / "worker-generate.py").read_text()
_sys_match = re.search(r'TOKE_SYSTEM_PROMPT = """(.*?)"""', _worker_py, re.DOTALL)
_rep_match = re.search(r'TOKE_REPAIR_PROMPT = """(.*?)"""', _worker_py, re.DOTALL)
TOKE_SYSTEM_PROMPT = _sys_match.group(1) if _sys_match else ""
TOKE_REPAIR_PROMPT = _rep_match.group(1) if _rep_match else ""

# Test programs to repair
TEST_IDS = [
    "AIA-001", "AIA-002", "AIA-003", "AIA-004",  # compile failures
    "AIA-018", "AIA-019",                          # build failures (missing main)
    "AIA-008", "AIA-043",                          # wrong output
    "AIA-033", "AIA-077",                          # segfault
]


def load_requirements() -> dict:
    reqs = {}
    for cat_dir in sorted(CATEGORIES_DIR.iterdir()):
        yaml_file = cat_dir / "requirements.yaml"
        if not yaml_file.exists():
            continue
        with open(yaml_file) as f:
            items = yaml.safe_load(f)
        if items:
            for item in items:
                reqs[item["id"]] = item
    return reqs


def find_solution(prog_id: str) -> Path | None:
    for p in SOLUTIONS_DIR.rglob(f"{prog_id}/solution.tk"):
        return p
    return None


def run_tkc_check(source_path: Path) -> tuple[bool, str]:
    try:
        r = subprocess.run([TKC, "--check", str(source_path)],
                          capture_output=True, text=True, timeout=60)
        return r.returncode == 0, (r.stdout + r.stderr).strip()
    except Exception as e:
        return False, str(e)


def run_tkc_build(source_path: Path, out_path: Path) -> tuple[bool, str]:
    try:
        r = subprocess.run([TKC, "--out", str(out_path), str(source_path)],
                          capture_output=True, text=True, timeout=60)
        return r.returncode == 0 and out_path.exists(), (r.stdout + r.stderr).strip()
    except Exception as e:
        return False, str(e)


def run_test(binary: Path, test_input: str, expected: str) -> tuple[bool, str]:
    try:
        r = subprocess.run([str(binary)], input=test_input,
                          capture_output=True, text=True, timeout=TEST_TIMEOUT)
        actual = r.stdout.strip()
        if r.returncode == -11:
            return False, "SEGFAULT"
        if actual == expected.strip():
            return True, actual
        return False, f"Expected: {expected.strip()!r}\nGot: {actual!r}"
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT"
    except Exception as e:
        return False, str(e)


def call_repair(source: str, error: str, description: str,
                test_input: str, expected_output: str,
                docs_context: str, history: list) -> str | None:
    user_content = TOKE_REPAIR_PROMPT.format(
        description=description,
        source=source,
        error=error,
        test_input=test_input[:200],
        expected_output=expected_output[:200],
    )
    if docs_context:
        user_content += "\n\nREFERENCE DOCUMENTATION:\n" + docs_context[:3000]

    messages = []
    if history:
        for h in history[-3:]:
            messages.append({"role": "user", "content":
                f"Fix this toke program.\nREQUIREMENT: {description}\n"
                f"```toke\n{h['source'][:2000]}\n```\nERROR:\n{h['error'][:800]}"})
            messages.append({"role": "assistant", "content":
                f"```toke\n{h.get('next_source', h['source'])[:2000]}\n```"})
    messages.append({"role": "user", "content": user_content})

    try:
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json",
            },
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 4096,
                "system": TOKE_SYSTEM_PROMPT,
                "messages": messages,
            },
            timeout=120,
        )
        resp.raise_for_status()
        text = resp.json()["content"][0]["text"]
        if "```toke" in text:
            text = text.split("```toke", 1)[1].split("```", 1)[0]
        elif "```" in text:
            text = text.split("```", 1)[1].split("```", 1)[0]
        return text.strip()
    except Exception as e:
        print(f"    API error: {e}")
        return None


def repair_program(prog_id: str, reqs: dict) -> dict:
    result = {"id": prog_id, "status": "UNKNOWN", "iterations": 0}

    sol_path = find_solution(prog_id)
    if not sol_path:
        result["status"] = "NO_SOURCE"
        return result

    source = sol_path.read_text()
    req = reqs.get(prog_id)
    if not req:
        result["status"] = "NO_REQUIREMENT"
        return result

    description = req.get("description", "")
    test_cases = req.get("test_cases", [])
    tc_input = test_cases[0].get("input", "") if test_cases else ""
    tc_expected = test_cases[0].get("expected_output", "") if test_cases else ""

    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        src = Path(tmpdir) / "prog.tk"
        binary = Path(tmpdir) / "prog"

        src.write_text(source)
        compiles, compile_out = run_tkc_check(src)
        if compiles:
            builds, build_out = run_tkc_build(src, binary)
            if builds:
                passes, test_out = run_test(binary, tc_input, tc_expected)
                if passes:
                    result["status"] = "ALREADY_PASS"
                    return result
                error = f"Test failures:\n{test_out}"
            else:
                error = f"Build error:\n{build_out}"
        else:
            error = f"Compile error:\n{compile_out}"

        # Repair loop
        conversation_history = []
        for iteration in range(1, MAX_ITERATIONS + 1):
            print(f"  Iteration {iteration}/{MAX_ITERATIONS}...", end=" ", flush=True)
            time.sleep(1)

            try:
                docs_context = rag_context(source, error)
            except Exception:
                docs_context = ""

            fixed = call_repair(source, error, description,
                               tc_input, tc_expected, docs_context,
                               conversation_history)
            if not fixed:
                print("no response")
                continue

            conversation_history.append({
                "source": source[:2000],
                "error": error[:800],
                "next_source": fixed[:2000],
            })

            source = fixed
            src.write_text(source)

            compiles, compile_out = run_tkc_check(src)
            if not compiles:
                error = f"Compile error:\n{compile_out}"
                print(f"compile fail")
                continue

            builds, build_out = run_tkc_build(src, binary)
            if not builds:
                error = f"Build error:\n{build_out}"
                print(f"build fail")
                continue

            passes, test_out = run_test(binary, tc_input, tc_expected)
            if passes:
                print(f"PASS!")
                result["status"] = "FIXED"
                result["iterations"] = iteration
                result["source"] = source
                return result
            else:
                error = f"Test failures:\n{test_out}"
                print(f"wrong output")

        result["status"] = "FAILED"
        result["iterations"] = MAX_ITERATIONS
        result["final_error"] = error[:500]
        return result


def main():
    if not ANTHROPIC_API_KEY:
        print("ERROR: Set ANTHROPIC_API_KEY environment variable")
        sys.exit(1)

    print(f"Loading requirements...")
    reqs = load_requirements()
    print(f"Loaded {len(reqs)} requirements\n")

    results = []
    for prog_id in TEST_IDS:
        print(f"[{prog_id}]")
        r = repair_program(prog_id, reqs)
        results.append(r)
        print(f"  → {r['status']} (iterations: {r['iterations']})\n")

    # Summary
    fixed = sum(1 for r in results if r["status"] == "FIXED")
    failed = sum(1 for r in results if r["status"] == "FAILED")
    other = sum(1 for r in results if r["status"] not in ("FIXED", "FAILED"))
    print(f"\n=== RESULTS ===")
    print(f"Fixed: {fixed}/{len(results)} ({fixed/len(results)*100:.0f}%)")
    print(f"Failed: {failed}/{len(results)}")
    if other:
        print(f"Other: {other}")
    for r in results:
        print(f"  {r['id']:10} {r['status']:12} iter={r['iterations']}")


if __name__ == "__main__":
    main()
