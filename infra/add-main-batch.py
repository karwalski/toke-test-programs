#!/usr/bin/env python3
"""add-main-batch.py — Add f=main() to programs missing entry points.

Reads programs from the missing-main list, sends each to Claude with the
original source + requirement, asking it to add a proper main function.
Processes in parallel batches of 10.
"""

import json
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests
import yaml

BASE_DIR = Path(__file__).resolve().parent.parent
SOLUTIONS_DIR = BASE_DIR / "results" / "solutions"
CATEGORIES_DIR = BASE_DIR / "categories"

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
TKC = "tkc"

SYSTEM_PROMPT = """You are fixing toke programs that are missing a main function entry point.

toke requires EVERY program to have f=main():$i64{...<0} as its entry point.

RULES:
- The main function must: read input with io.readln(), call the existing functions, print output with io.println(), and return <0
- Import std.io and std.str if not already imported: i=io:std.io; i=s:std.str;
- Semicolons separate ALL parameters and statements. NEVER commas.
- Parse input: let n=s.toint(io.readln()); or let line=io.readln();
- Convert to string for output: io.println(s.fromint(result)) or io.println(result) if already a string
- int to string: s.fromint(n) or n as$str
- The existing functions in the source are correct — do NOT modify them. ONLY add main + needed imports.
- No uppercase, no underscores in identifiers.
- NEVER use i/f/t/m as variable names.

Output ONLY the complete fixed source code. No explanation."""

ADD_MAIN_PROMPT = """This toke program compiles but has no main function, so it can't link.

REQUIREMENT: {description}
INPUT FORMAT: {input_format}
OUTPUT FORMAT: {output_format}
TEST INPUT: {test_input}
EXPECTED OUTPUT: {expected_output}

CURRENT SOURCE (has functions but NO main):
```toke
{source}
```

Add a f=main():$i64{{...<0}} function that:
1. Reads input using io.readln()
2. Parses it appropriately (s.toint for numbers, s.split for multiple values)
3. Calls the existing function(s) with the parsed input
4. Prints the result using io.println()
5. Returns <0

Add any missing imports (i=io:std.io; i=s:std.str;) AFTER the m= line and BEFORE f= declarations.
Do NOT modify existing functions — only ADD main and imports.

Return the COMPLETE source code in ```toke``` markers."""


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


def call_claude(source: str, req: dict) -> str | None:
    tc = req.get("test_cases", [{}])[0] if req.get("test_cases") else {}
    prompt = ADD_MAIN_PROMPT.format(
        description=req.get("description", ""),
        input_format=req.get("input_format", ""),
        output_format=req.get("output_format", ""),
        test_input=tc.get("input", "")[:300],
        expected_output=tc.get("expected_output", "")[:300],
        source=source,
    )
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
                "system": SYSTEM_PROMPT,
                "messages": [{"role": "user", "content": prompt}],
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
        return None


def test_program(source: str, req: dict, tmpdir: Path) -> tuple[str, str]:
    """Returns (status, detail)"""
    src = tmpdir / "prog.tk"
    binary = tmpdir / "prog"
    src.write_text(source)

    # Compile
    r = subprocess.run([TKC, "--check", str(src)], capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        return "COMPILE_FAIL", (r.stdout + r.stderr)[:300]

    # Build
    r = subprocess.run([TKC, "--out", str(binary), str(src)], capture_output=True, text=True, timeout=60)
    if r.returncode != 0 or not binary.exists():
        return "BUILD_FAIL", (r.stdout + r.stderr)[:300]

    # Run test
    tc = req.get("test_cases", [{}])[0] if req.get("test_cases") else {}
    test_input = tc.get("input", "")
    expected = tc.get("expected_output", "").strip()
    try:
        r = subprocess.run([str(binary)], input=test_input,
                          capture_output=True, text=True, timeout=10)
        actual = r.stdout.strip()
        if r.returncode == -11:
            return "SEGFAULT", ""
        if actual == expected:
            return "PASS", actual
        return "WRONG_OUTPUT", f"expected={expected!r} got={actual!r}"
    except subprocess.TimeoutExpired:
        return "TIMEOUT", ""
    except Exception as e:
        return "RUN_FAIL", str(e)


def process_one(prog_id: str, reqs: dict) -> dict:
    result = {"id": prog_id}
    sol = find_solution(prog_id)
    if not sol:
        result["status"] = "NO_SOURCE"
        return result

    source = sol.read_text()
    req = reqs.get(prog_id)
    if not req:
        result["status"] = "NO_REQ"
        return result

    # Call Claude to add main
    fixed = call_claude(source, req)
    if not fixed:
        result["status"] = "API_FAIL"
        return result

    # Test the fixed version
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        status, detail = test_program(fixed, req, Path(tmpdir))

    result["status"] = status
    result["detail"] = detail[:200]

    # If it at least builds, save the fixed source
    if status in ("PASS", "WRONG_OUTPUT", "RUN_FAIL", "SEGFAULT", "TIMEOUT"):
        sol.write_text(fixed)
        result["saved"] = True
    elif status == "COMPILE_FAIL":
        # Still save if it's better than no main at all
        # Check: does fixed have f=main?
        if "f=main" in fixed:
            sol.write_text(fixed)
            result["saved"] = True

    return result


def main():
    if not ANTHROPIC_API_KEY:
        print("ERROR: Set ANTHROPIC_API_KEY")
        sys.exit(1)

    with open("/tmp/missing_main_ids.json") as f:
        prog_ids = json.load(f)

    print(f"Loading requirements...")
    reqs = load_requirements()
    print(f"Processing {len(prog_ids)} programs in batches of 10...\n")

    results = []
    batch_size = 10
    max_workers = 5

    for batch_start in range(0, len(prog_ids), batch_size):
        batch = prog_ids[batch_start:batch_start + batch_size]
        batch_num = batch_start // batch_size + 1
        total_batches = (len(prog_ids) + batch_size - 1) // batch_size
        print(f"Batch {batch_num}/{total_batches}: {batch}")

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(process_one, pid, reqs): pid for pid in batch}
            for future in as_completed(futures):
                r = future.result()
                results.append(r)
                saved = " [SAVED]" if r.get("saved") else ""
                print(f"  {r['id']:10} → {r['status']}{saved}")

        # Rate limit between batches
        time.sleep(1)

    # Summary
    from collections import Counter
    stats = Counter(r["status"] for r in results)
    print(f"\n=== RESULTS ({len(results)} programs) ===")
    for status, count in stats.most_common():
        print(f"  {status}: {count}")

    saved = sum(1 for r in results if r.get("saved"))
    print(f"\nSaved: {saved}/{len(results)}")

    with open(BASE_DIR / "results" / "add-main-report.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"Report: results/add-main-report.json")


if __name__ == "__main__":
    main()
