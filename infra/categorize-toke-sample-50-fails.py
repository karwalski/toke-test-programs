#!/usr/bin/env python3
"""categorize-toke-sample-50-fails.py — classify the 45 failures from the
sample-50 toke repair run.

For each failed program:
  1. Locate the Opus output: results/toke-sample-50/attempts/<id>/iter-01-opus.tk
  2. Re-test with current local tkc:
     - compile (tkc --check)
     - build   (tkc --out)
     - run     (execute on first test case's input, compare to expected_output)
  3. Classify the failure into one of:
       compile_fail        — tkc rejects the source
       build_fail          — compiles but link/build step errors
       runtime_crash       — runs but non-zero exit / segfault
       runtime_timeout     — exceeded 10s
       empty_output        — runs, exit 0, but printed nothing
       wrong_output        — runs cleanly, output != expected
       output_close        — output close-ish (length within ±20%, prefix matches)
       worker_misclassified — passes our local test (worker bug)

Then surface patterns: top error codes, missing-print issues, signature gaps.
"""

import json
import os
import re
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

import yaml

BASE = Path(__file__).resolve().parent.parent
ATTEMPTS = BASE / "results" / "toke-sample-50" / "attempts"
CATEGORIES = BASE / "categories"
TAGS = BASE / "results" / "tagged-toke-sample-50.json"
TKC = os.environ.get("TKC", "/Users/matthew.watt/tk/toke/tkc")


def load_requirements() -> dict:
    """{id: spec_dict}."""
    out = {}
    for req in CATEGORIES.glob("*/requirements.yaml"):
        try:
            specs = yaml.safe_load(req.read_text())
        except Exception:
            continue
        for s in specs or []:
            if "id" in s:
                out[s["id"]] = s
    return out


def compile_check(src_path: Path) -> tuple[bool, str]:
    try:
        r = subprocess.run([TKC, "--check", str(src_path)], capture_output=True, text=True, timeout=30)
        return r.returncode == 0, (r.stdout + r.stderr).strip()
    except Exception as e:
        return False, f"check-err: {e}"


def build(src_path: Path, out_path: Path) -> tuple[bool, str]:
    try:
        r = subprocess.run([TKC, "--out", str(out_path), str(src_path)], capture_output=True, text=True, timeout=60)
        return r.returncode == 0 and out_path.exists(), (r.stdout + r.stderr).strip()
    except Exception as e:
        return False, f"build-err: {e}"


def run_one(bin_path: Path, stdin: str) -> tuple[int, str, str]:
    try:
        r = subprocess.run([str(bin_path)], input=stdin, capture_output=True, text=True, timeout=10)
        return r.returncode, r.stdout, r.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "TIMEOUT"
    except Exception as e:
        return -2, "", f"runner-err: {e}"


def extract_error_codes(text: str) -> list[str]:
    return re.findall(r'\bE\d{4}\b', text)


def classify(prog_id: str, spec: dict, opus_src: Path) -> dict:
    result = {"id": prog_id, "category": "?"}

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        # Stage as solution.tk
        staged = td / "solution.tk"
        staged.write_text(opus_src.read_text())

        # Compile
        compiles, comp_out = compile_check(staged)
        if not compiles:
            result["category"] = "compile_fail"
            result["error_codes"] = extract_error_codes(comp_out)
            result["error_excerpt"] = comp_out[:300]
            return result

        # Build
        bin_path = td / "bin"
        built, build_out = build(staged, bin_path)
        if not built:
            result["category"] = "build_fail"
            result["error_codes"] = extract_error_codes(build_out)
            result["error_excerpt"] = build_out[:300]
            return result

        # Run all test cases (record first-fail details)
        tcs = spec.get("test_cases", []) if spec else []
        if not tcs:
            result["category"] = "no_test_cases"
            return result

        per_test = []
        all_pass = True
        first_actual = first_expected = first_stderr = ""
        first_rc = 0
        for tc in tcs:
            stdin = tc.get("input", "") or ""
            expected = (tc.get("expected_output", "") or "").rstrip("\n")
            rc, stdout, stderr = run_one(bin_path, stdin)
            actual = stdout.rstrip("\n")
            ok = (rc == 0 and actual == expected)
            per_test.append({"pass": ok, "rc": rc})
            if not ok and not first_stderr and not first_actual:
                first_actual, first_expected, first_stderr, first_rc = actual, expected, stderr, rc
            if not ok:
                all_pass = False
        if all_pass:
            result["category"] = "worker_misclassified"
            result["per_test"] = per_test
            return result

        # Sub-categorize the failure
        if first_rc == -1:
            result["category"] = "runtime_timeout"
        elif first_rc < 0:
            result["category"] = "runner_error"
        elif first_rc != 0:
            result["category"] = "runtime_crash"
            result["rc"] = first_rc
            result["stderr_excerpt"] = first_stderr[:200]
        elif first_actual == "":
            result["category"] = "empty_output"
            result["expected_excerpt"] = first_expected[:200]
        else:
            # output exists but doesn't match
            ratio = len(first_actual) / max(len(first_expected), 1)
            if 0.5 <= ratio <= 2.0 and first_expected and first_actual[:20] == first_expected[:20]:
                result["category"] = "output_close"
            else:
                result["category"] = "wrong_output"
            result["actual_excerpt"] = first_actual[:200]
            result["expected_excerpt"] = first_expected[:200]
        return result


def main():
    tags = json.loads(TAGS.read_text())
    passed_ids = set()
    state_files = sorted((BASE / "results" / "toke-sample-50").glob("state-w*.json"))
    for sf in state_files:
        s = json.loads(sf.read_text())
        for pid in s.get("completed", []):
            passed_ids.add(pid)

    reqs = load_requirements()
    all_ids = [t["id"] for t in tags["tags"]]
    fail_ids = [pid for pid in all_ids if pid not in passed_ids]
    print(f"Re-classifying {len(fail_ids)} failures (with current local tkc)\n")

    results = []
    for pid in sorted(fail_ids):
        opus = ATTEMPTS / pid / "iter-01-opus.tk"
        if not opus.exists():
            results.append({"id": pid, "category": "no_opus_output"})
            continue
        r = classify(pid, reqs.get(pid), opus)
        # Pull tag category for context
        for t in tags["tags"]:
            if t["id"] == pid:
                r["program_category"] = t["category"]
                r["original_status"] = t["status"]
                break
        results.append(r)

    # Aggregate
    cat_counts = Counter(r["category"] for r in results)
    print("=== Failure categories ===")
    for cat, n in cat_counts.most_common():
        print(f"  {n:3d}  {cat}")

    # Error code frequencies (for compile/build fails)
    ec = Counter()
    for r in results:
        for c in r.get("error_codes", []):
            ec[c] += 1
    if ec:
        print("\n=== Compile/build error codes ===")
        for c, n in ec.most_common(10):
            print(f"  {n:3d}  {c}")

    # Per program-category breakdown
    by_progcat = defaultdict(Counter)
    for r in results:
        by_progcat[r.get("program_category", "?")][r["category"]] += 1
    print("\n=== Failures per program-category ===")
    for pc in sorted(by_progcat):
        print(f"  {pc}: {dict(by_progcat[pc])}")

    # List per-program one-liner
    print("\n=== Per-program detail ===")
    for r in sorted(results, key=lambda x: (x["category"], x["id"])):
        line = f"  {r['id']:<10} [{r['program_category']:<20}] {r['category']:<22}"
        if r["category"] in ("compile_fail", "build_fail"):
            line += f" codes={r.get('error_codes', [])}"
        elif r["category"] == "wrong_output":
            line += f" got={r.get('actual_excerpt','')[:50]!r} want={r.get('expected_excerpt','')[:50]!r}"
        elif r["category"] == "empty_output":
            line += f" expected={r.get('expected_excerpt','')[:60]!r}"
        elif r["category"] == "runtime_crash":
            line += f" rc={r.get('rc')} stderr={r.get('stderr_excerpt','')[:60]!r}"
        print(line)

    # Save full detail
    out_file = BASE / "results" / "toke-sample-50" / "fail-categorization.json"
    out_file.write_text(json.dumps(results, indent=2))
    print(f"\nFull detail: {out_file}")


if __name__ == "__main__":
    main()
