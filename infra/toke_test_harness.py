"""toke_test_harness.py — shared compile/build/test/classify primitives.

Consolidates fragments previously scattered across:
  - infra/local-audit.py
  - infra/local-repair-test.py
  - infra/categorize-toke-sample-50-fails.py

The remote `infra/worker-generate.py` keeps its OWN copies of compile/build/
test (since workers run without this module) but this harness replicates
their behaviour byte-for-byte so local dry-runs match real workers.

Story 107.R4.6.
"""

from __future__ import annotations

import os
import re
import subprocess
import tempfile
from pathlib import Path

TKC = os.environ.get("TKC", "tkc")
TKC_TIMEOUT = int(os.environ.get("TKC_TIMEOUT", "60"))
TEST_TIMEOUT = int(os.environ.get("TEST_TIMEOUT", "10"))


# ----------------------------------------------------------------------------
# Compile + build wrappers
# ----------------------------------------------------------------------------
def compile_check(source_path: Path) -> tuple[bool, str]:
    """Run `tkc --check <src>`. Returns (success, combined_output)."""
    try:
        r = subprocess.run(
            [TKC, "--check", str(source_path)],
            capture_output=True, text=True, timeout=TKC_TIMEOUT,
            errors="replace",
        )
        return r.returncode == 0, (r.stdout + r.stderr).strip()
    except subprocess.TimeoutExpired:
        return False, f"TIMEOUT: tkc --check exceeded {TKC_TIMEOUT}s"
    except FileNotFoundError:
        return False, f"ERROR: {TKC} not found in PATH"
    except Exception as e:
        return False, f"ERROR: {e}"


def build(source_path: Path, output_path: Path) -> tuple[bool, str]:
    """Run `tkc --out <out> <src>`. Returns (success, combined_output)."""
    try:
        r = subprocess.run(
            [TKC, "--out", str(output_path), str(source_path)],
            capture_output=True, text=True, timeout=TKC_TIMEOUT,
            errors="replace",
        )
        output = (r.stdout + r.stderr).strip()
        if r.returncode != 0:
            return False, output
        if not output_path.exists():
            return False, "Binary not produced"
        return True, output
    except subprocess.TimeoutExpired:
        return False, f"TIMEOUT: tkc --out exceeded {TKC_TIMEOUT}s"
    except Exception as e:
        return False, f"ERROR: {e}"


# ----------------------------------------------------------------------------
# Output normalisation (tolerant comparison)
# ----------------------------------------------------------------------------
def normalize(s: str) -> str:
    """Collapse whitespace, strip lines, normalize line endings."""
    s = s.strip()
    s = re.sub(r'[ \t]+', ' ', s)
    s = s.replace('\r\n', '\n').replace('\r', '\n')
    return '\n'.join(line.rstrip() for line in s.split('\n'))


def floats_close(actual: str, expected: str, rel_tol: float = 0.01) -> bool:
    """True if all numbers in actual match expected within rel_tol, and the
    non-numeric text scaffolding matches after normalisation."""
    a_nums = re.findall(r'-?\d+\.?\d*(?:[eE][+-]?\d+)?', actual)
    e_nums = re.findall(r'-?\d+\.?\d*(?:[eE][+-]?\d+)?', expected)
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
        a_text = re.sub(r'-?\d+\.?\d*(?:[eE][+-]?\d+)?', '#', actual)
        e_text = re.sub(r'-?\d+\.?\d*(?:[eE][+-]?\d+)?', '#', expected)
        return normalize(a_text) == normalize(e_text)
    except (ValueError, ZeroDivisionError):
        return False


def order_insensitive_match(actual: str, expected: str) -> bool:
    a_tokens = sorted(actual.split())
    e_tokens = sorted(expected.split())
    return a_tokens == e_tokens and len(a_tokens) > 1


# ----------------------------------------------------------------------------
# Test runner
# ----------------------------------------------------------------------------
def run_test(binary_path: Path, test_input: str, expected_output: str) -> tuple[bool, str, str]:
    """Run binary with input, compare output. Returns (passed, actual_output, error_msg).

    Tiered matching: exact → normalized whitespace → float tolerance (±1%) →
    order-insensitive tokens.
    """
    try:
        r = subprocess.run(
            [str(binary_path)],
            input=test_input, capture_output=True, text=True, timeout=TEST_TIMEOUT,
            errors="replace",
        )
        actual = (r.stdout or "").strip()
        expected = (expected_output or "").strip()
        if r.returncode == -11 or r.returncode == 139:
            return False, actual, "SEGFAULT"
        if r.returncode != 0:
            return False, actual, f"Exit {r.returncode}: {(r.stderr or '').strip()[:500]}"
        if actual == expected:
            return True, actual, ""
        if normalize(actual) == normalize(expected):
            return True, actual, ""
        if floats_close(actual, expected):
            return True, actual, ""
        if order_insensitive_match(normalize(actual), normalize(expected)):
            return True, actual, ""
        return False, actual, f"Expected: {expected!r}\nGot: {actual!r}"
    except subprocess.TimeoutExpired:
        return False, "", f"TIMEOUT: test exceeded {TEST_TIMEOUT}s"
    except Exception as e:
        return False, "", f"ERROR: {e}"


# ----------------------------------------------------------------------------
# Diagnostic helpers
# ----------------------------------------------------------------------------
def extract_error_codes(output: str) -> list[str]:
    """Pull E#### codes from tkc diagnostic output, preserving order + duplicates."""
    return re.findall(r'\bE\d{4}\b', output)


# ----------------------------------------------------------------------------
# Failure classification (mirrors categorize-toke-sample-50-fails.py)
# ----------------------------------------------------------------------------
def classify_failure(opus_src: str, test_cases: list) -> dict:
    """Run opus_src through compile + build + every test_case. Return a dict
    with `category` ∈ {compile_fail, build_fail, runtime_crash, runtime_timeout,
    empty_output, wrong_output, output_close, worker_misclassified, no_test_cases,
    runner_error}, plus diagnostic details."""
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        staged = td / "solution.tk"
        staged.write_text(opus_src)

        ok, out = compile_check(staged)
        if not ok:
            return {
                "category": "compile_fail",
                "error_codes": extract_error_codes(out),
                "error_excerpt": out[:300],
            }

        bin_path = td / "bin"
        ok, out = build(staged, bin_path)
        if not ok:
            return {
                "category": "build_fail",
                "error_codes": extract_error_codes(out),
                "error_excerpt": out[:300],
            }

        if not test_cases:
            return {"category": "no_test_cases"}

        per_test = []
        all_pass = True
        first_actual = first_expected = first_stderr = ""
        first_rc = 0
        for tc in test_cases:
            stdin = tc.get("input", "") or ""
            expected = (tc.get("expected_output", "") or "").rstrip("\n")
            ok, actual, err = run_test(bin_path, stdin, expected)
            try:
                r = subprocess.run([str(bin_path)], input=stdin, capture_output=True,
                                   text=True, timeout=TEST_TIMEOUT, errors="replace")
                rc, stdout, stderr = r.returncode, r.stdout, r.stderr
            except subprocess.TimeoutExpired:
                rc, stdout, stderr = -1, "", "TIMEOUT"
            actual_raw = stdout.rstrip("\n")
            per_test.append({"pass": ok, "rc": rc})
            if not ok and not first_stderr and not first_actual:
                first_actual, first_expected, first_stderr, first_rc = actual_raw, expected, stderr, rc
            if not ok:
                all_pass = False

        if all_pass:
            return {"category": "worker_misclassified", "per_test": per_test}

        if first_rc == -1:
            return {"category": "runtime_timeout"}
        if first_rc < 0:
            return {"category": "runner_error"}
        if first_rc != 0:
            return {
                "category": "runtime_crash",
                "rc": first_rc,
                "stderr_excerpt": first_stderr[:200],
            }
        if first_actual == "":
            return {
                "category": "empty_output",
                "expected_excerpt": first_expected[:200],
            }
        ratio = len(first_actual) / max(len(first_expected), 1)
        if 0.5 <= ratio <= 2.0 and first_expected and first_actual[:20] == first_expected[:20]:
            cat = "output_close"
        else:
            cat = "wrong_output"
        return {
            "category": cat,
            "actual_excerpt": first_actual[:200],
            "expected_excerpt": first_expected[:200],
        }
