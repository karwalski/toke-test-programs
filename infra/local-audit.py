#!/usr/bin/env python3
"""local-audit.py — Recompile and retest all solutions locally.

Reads solutions from results/solutions/, matches against requirements in
categories/*/requirements.yaml, and classifies each program:
  PASS, COMPILE_FAIL, BUILD_FAIL, RUN_FAIL, WRONG_OUTPUT, NO_TEST_CASE

Outputs results/audit-report.json with per-program status and errors.
"""

import json
import os
import subprocess
import sys
import tempfile
import time
import yaml
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).resolve().parent.parent
SOLUTIONS_DIR = BASE_DIR / "results" / "solutions"
CATEGORIES_DIR = BASE_DIR / "categories"
REPORT_PATH = BASE_DIR / "results" / "audit-report.json"

TKC = os.environ.get("TKC", "tkc")
TKC_TIMEOUT = 60
TEST_TIMEOUT = 10


def load_requirements() -> dict:
    """Load all requirements keyed by ID."""
    reqs = {}
    for cat_dir in sorted(CATEGORIES_DIR.iterdir()):
        yaml_file = cat_dir / "requirements.yaml"
        if not yaml_file.exists():
            continue
        with open(yaml_file) as f:
            items = yaml.safe_load(f)
        if not items:
            continue
        for item in items:
            reqs[item["id"]] = item
    return reqs


def run_tkc_check(source_path: Path) -> tuple[bool, str]:
    """Run tkc --check on a source file."""
    try:
        result = subprocess.run(
            [TKC, "--check", str(source_path)],
            capture_output=True, text=True, timeout=TKC_TIMEOUT,
        )
        output = (result.stdout + result.stderr).strip()
        return result.returncode == 0, output
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT: tkc --check exceeded 60s"
    except Exception as e:
        return False, f"ERROR: {e}"


def run_tkc_build(source_path: Path, output_path: Path) -> tuple[bool, str]:
    """Compile source to binary."""
    try:
        result = subprocess.run(
            [TKC, "--out", str(output_path), str(source_path)],
            capture_output=True, text=True, timeout=TKC_TIMEOUT,
        )
        output = (result.stdout + result.stderr).strip()
        if result.returncode != 0:
            return False, output
        if not output_path.exists():
            return False, "Binary not produced"
        return True, output
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT: tkc --out exceeded 60s"
    except Exception as e:
        return False, f"ERROR: {e}"


def _normalize(s: str) -> str:
    """Normalize output for tolerant comparison: collapse whitespace, strip."""
    import re as _re
    s = s.strip()
    # Collapse multiple spaces/tabs to single space
    s = _re.sub(r'[ \t]+', ' ', s)
    # Normalize line endings
    s = s.replace('\r\n', '\n').replace('\r', '\n')
    # Strip trailing whitespace per line
    s = '\n'.join(line.rstrip() for line in s.split('\n'))
    return s


def _floats_close(actual: str, expected: str, rel_tol: float = 0.01) -> bool:
    """Check if all numbers in actual and expected are within relative tolerance."""
    import re as _re
    a_nums = _re.findall(r'-?\d+\.?\d*(?:[eE][+-]?\d+)?', actual)
    e_nums = _re.findall(r'-?\d+\.?\d*(?:[eE][+-]?\d+)?', expected)
    if not a_nums or not e_nums or len(a_nums) != len(e_nums):
        return False
    try:
        for a, e in zip(a_nums, e_nums):
            af, ef = float(a), float(e)
            if ef == 0:
                if abs(af) > 0.001:
                    return False
            elif abs(af - ef) / max(abs(ef), 1e-9) > rel_tol:
                return False
        # Also check that the non-numeric parts match
        a_text = _re.sub(r'-?\d+\.?\d*(?:[eE][+-]?\d+)?', '#', actual)
        e_text = _re.sub(r'-?\d+\.?\d*(?:[eE][+-]?\d+)?', '#', expected)
        if _normalize(a_text) != _normalize(e_text):
            return False
        return True
    except (ValueError, ZeroDivisionError):
        return False


def _order_insensitive_match(actual: str, expected: str) -> bool:
    """Check if actual and expected have the same tokens in any order."""
    a_tokens = sorted(actual.split())
    e_tokens = sorted(expected.split())
    return a_tokens == e_tokens and len(a_tokens) > 1


def run_test(binary_path: Path, test_input: str, expected_output: str) -> tuple[bool, str, str]:
    """Run binary with input, compare output. Returns (passed, actual_output, error).

    Comparison uses tiered matching:
    1. Exact match (after strip)
    2. Normalized match (collapsed whitespace, stripped lines)
    3. Float tolerance (±1% relative)
    4. Order-insensitive match (same tokens, different order)
    """
    try:
        result = subprocess.run(
            [str(binary_path)],
            input=test_input, capture_output=True, text=True, timeout=TEST_TIMEOUT,
        )
        actual = result.stdout.strip()
        expected = expected_output.strip()
        if result.returncode != 0 and result.returncode != -11:
            stderr = result.stderr.strip()[:500]
            return False, actual, f"Exit code {result.returncode}: {stderr}"
        if result.returncode == -11:
            return False, actual, "SEGFAULT"
        # Tier 1: exact match
        if actual == expected:
            return True, actual, ""
        # Tier 2: normalized whitespace match
        if _normalize(actual) == _normalize(expected):
            return True, actual, ""
        # Tier 3: float tolerance (±1%)
        if _floats_close(actual, expected):
            return True, actual, ""
        # Tier 4: order-insensitive match
        if _order_insensitive_match(_normalize(actual), _normalize(expected)):
            return True, actual, ""
        return False, actual, f"Expected: {repr(expected)}\nGot: {repr(actual)}"
    except subprocess.TimeoutExpired:
        return False, "", "TIMEOUT: test exceeded 10s"
    except Exception as e:
        return False, "", f"ERROR: {e}"


def extract_error_codes(output: str) -> list[str]:
    """Extract E-codes from compiler output."""
    import re
    return re.findall(r'E\d{4}', output)


def audit_program(prog_id: str, category: str, solution_path: Path,
                  req: dict | None, work_dir: Path) -> dict:
    """Audit a single program. Returns result dict."""
    source_path = solution_path / "solution.tk"
    if not source_path.exists():
        return {"id": prog_id, "category": category, "status": "NO_SOURCE"}

    source_size = source_path.stat().st_size
    result = {
        "id": prog_id,
        "category": category,
        "source_bytes": source_size,
    }

    # Step 1: Compile check
    compiles, compile_output = run_tkc_check(source_path)
    if not compiles:
        result["status"] = "COMPILE_FAIL"
        result["error"] = compile_output[:2000]
        result["error_codes"] = extract_error_codes(compile_output)
        return result

    # Step 2: Build
    binary_path = work_dir / prog_id
    builds, build_output = run_tkc_build(source_path, binary_path)
    if not builds:
        result["status"] = "BUILD_FAIL"
        result["error"] = build_output[:2000]
        result["error_codes"] = extract_error_codes(build_output)
        return result

    # Step 3: Test
    if not req:
        result["status"] = "NO_TEST_CASE"
        result["note"] = "Compiles and builds but no requirement found to test against"
        return result

    test_cases = req.get("test_cases", [])
    if not test_cases:
        result["status"] = "NO_TEST_CASE"
        result["note"] = "Requirement has no test cases"
        return result

    # Run first test case
    tc = test_cases[0]
    test_input = tc.get("input", "")
    expected_output = tc.get("expected_output", "")

    passes, actual, error = run_test(binary_path, test_input, expected_output)
    if passes:
        result["status"] = "PASS"
        # Run remaining test cases
        all_pass = True
        for i, tc2 in enumerate(test_cases[1:], 2):
            p2, a2, e2 = run_test(binary_path, tc2.get("input", ""), tc2.get("expected_output", ""))
            if not p2:
                result["status"] = "WRONG_OUTPUT"
                result["error"] = f"Test case {i} failed: {e2}"
                result["actual_output"] = a2
                all_pass = False
                break
        if all_pass:
            result["status"] = "PASS"
            result["test_cases_passed"] = len(test_cases)
    else:
        if "SEGFAULT" in error:
            result["status"] = "RUN_FAIL"
        elif "TIMEOUT" in error:
            result["status"] = "RUN_FAIL"
        elif "Exit code" in error:
            result["status"] = "RUN_FAIL"
        else:
            result["status"] = "WRONG_OUTPUT"
        result["error"] = error[:1000]
        result["actual_output"] = actual[:500]

    # Cleanup binary
    if binary_path.exists():
        binary_path.unlink()

    return result


def main():
    print("Loading requirements...")
    reqs = load_requirements()
    print(f"Loaded {len(reqs)} requirements")

    # Find all solutions
    programs = []
    for cat_dir in sorted(SOLUTIONS_DIR.iterdir()):
        if not cat_dir.is_dir():
            continue
        category = cat_dir.name
        for prog_dir in sorted(cat_dir.iterdir()):
            if not prog_dir.is_dir():
                continue
            prog_id = prog_dir.name
            programs.append((prog_id, category, prog_dir))

    print(f"Found {len(programs)} solutions to audit")

    results = []
    stats = defaultdict(int)
    category_stats = defaultdict(lambda: defaultdict(int))

    with tempfile.TemporaryDirectory(prefix="toke-audit-") as work_dir:
        work_path = Path(work_dir)
        for i, (prog_id, category, solution_path) in enumerate(programs):
            r = audit_program(prog_id, category, solution_path, reqs.get(prog_id), work_path)
            results.append(r)
            stats[r["status"]] += 1
            category_stats[category][r["status"]] += 1

            # Progress
            if (i + 1) % 50 == 0 or i == len(programs) - 1:
                print(f"  [{i+1}/{len(programs)}] "
                      f"PASS={stats['PASS']} COMPILE_FAIL={stats['COMPILE_FAIL']} "
                      f"BUILD_FAIL={stats['BUILD_FAIL']} RUN_FAIL={stats['RUN_FAIL']} "
                      f"WRONG_OUTPUT={stats['WRONG_OUTPUT']} NO_TEST={stats['NO_TEST_CASE']}")

    # Build report
    report = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tkc_version": subprocess.run([TKC, "--version"], capture_output=True, text=True).stdout.strip(),
        "total_programs": len(programs),
        "summary": dict(stats),
        "category_summary": {k: dict(v) for k, v in sorted(category_stats.items())},
        "programs": results,
    }

    # Error code frequency
    error_codes = defaultdict(int)
    for r in results:
        for code in r.get("error_codes", []):
            error_codes[code] += 1
    report["error_code_frequency"] = dict(sorted(error_codes.items(), key=lambda x: -x[1]))

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_PATH, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\n=== AUDIT COMPLETE ===")
    print(f"Report: {REPORT_PATH}")
    print(f"\nSummary:")
    for status, count in sorted(stats.items(), key=lambda x: -x[1]):
        pct = count / len(programs) * 100
        print(f"  {status}: {count} ({pct:.1f}%)")

    if error_codes:
        print(f"\nTop error codes:")
        for code, count in sorted(error_codes.items(), key=lambda x: -x[1])[:10]:
            print(f"  {code}: {count}")


if __name__ == "__main__":
    main()
