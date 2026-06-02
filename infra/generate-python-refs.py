#!/usr/bin/env python3
"""generate-python-refs.py — Generate Python reference implementations for all programs.

For each program requirement, generates a Python solution and tests it against
the expected output. This validates that the test cases are correct and provides
a baseline for token comparison.

Output per program:
  results/python-refs/<category>/<id>/solution.py  — Python implementation
  results/python-refs/<category>/<id>/output.txt   — actual output
  results/python-refs/<category>/<id>/status.json   — pass/fail/error details
"""

import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests
import yaml

BASE_DIR = Path(__file__).resolve().parent.parent
CATEGORIES_DIR = BASE_DIR / "categories"
PYTHON_REFS_DIR = BASE_DIR / "results" / "python-refs"
REPORT_PATH = BASE_DIR / "results" / "python-validation-report.json"

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
TEST_TIMEOUT = 10
BATCH_SIZE = 10
MAX_WORKERS = 5

PYTHON_GEN_PROMPT = """Write a Python 3 program that solves this requirement.

REQUIREMENT: {description}
INPUT FORMAT: {input_format}
OUTPUT FORMAT: {output_format}
TEST INPUT: {test_input}
EXPECTED OUTPUT: {expected_output}

Rules:
- Read from stdin, write to stdout
- Output must EXACTLY match the expected output (whitespace-sensitive)
- Use ONLY Python 3 standard library — NO pip packages (no cryptography, no websockets, no requests, no base58, no Crypto)
- For crypto: use hashlib, hmac, secrets from stdlib. For base64: use base64 module. Implement simple algorithms directly.
- For networking: simulate the behavior, don't actually open sockets or start servers. Print the expected output directly based on the input.
- The program must complete within 10 seconds — NO infinite loops, NO server listen loops, NO blocking waits
- Keep it simple and correct — no fancy frameworks
- Handle the input format exactly as described

Return ONLY the Python code in ```python ... ``` markers."""


def load_requirements() -> list[dict]:
    reqs = []
    for cat_dir in sorted(CATEGORIES_DIR.iterdir()):
        yaml_file = cat_dir / "requirements.yaml"
        if not yaml_file.exists():
            continue
        with open(yaml_file) as f:
            items = yaml.safe_load(f)
        if items:
            for item in items:
                item["_category"] = cat_dir.name
                reqs.append(item)
    return reqs


def generate_python(req: dict) -> str | None:
    tc = req.get("test_cases", [{}])[0] if req.get("test_cases") else {}
    prompt = PYTHON_GEN_PROMPT.format(
        description=req.get("description", ""),
        input_format=req.get("input_format", ""),
        output_format=req.get("output_format", ""),
        test_input=tc.get("input", "")[:500],
        expected_output=tc.get("expected_output", "")[:500],
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
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=120,
        )
        resp.raise_for_status()
        text = resp.json()["content"][0]["text"]
        if "```python" in text:
            text = text.split("```python", 1)[1].split("```", 1)[0]
        elif "```" in text:
            text = text.split("```", 1)[1].split("```", 1)[0]
        return text.strip()
    except Exception as e:
        return None


def _normalize(s: str) -> str:
    s = s.strip()
    s = re.sub(r'[ \t]+', ' ', s)
    s = s.replace('\r\n', '\n').replace('\r', '\n')
    s = '\n'.join(line.rstrip() for line in s.split('\n'))
    return s


def _floats_close(actual: str, expected: str, rel_tol: float = 0.01) -> bool:
    a_nums = re.findall(r'-?\d+\.?\d*(?:[eE][+-]?\d+)?', actual)
    e_nums = re.findall(r'-?\d+\.?\d*(?:[eE][+-]?\d+)?', expected)
    if not a_nums or not e_nums or len(a_nums) != len(e_nums):
        return False
    try:
        for a, e in zip(a_nums, e_nums):
            af, ef = float(a), float(e)
            if ef == 0:
                if abs(af) > 0.001: return False
            elif abs(af - ef) / max(abs(ef), 1e-9) > rel_tol:
                return False
        a_text = re.sub(r'-?\d+\.?\d*(?:[eE][+-]?\d+)?', '#', actual)
        e_text = re.sub(r'-?\d+\.?\d*(?:[eE][+-]?\d+)?', '#', expected)
        if _normalize(a_text) != _normalize(e_text): return False
        return True
    except (ValueError, ZeroDivisionError):
        return False


def _order_insensitive(actual: str, expected: str) -> bool:
    a_tokens = sorted(actual.split())
    e_tokens = sorted(expected.split())
    return a_tokens == e_tokens and len(a_tokens) > 1


def test_python(source: str, test_input: str, expected: str) -> dict:
    try:
        r = subprocess.run(
            [sys.executable, "-c", source],
            input=test_input, capture_output=True, text=True, timeout=TEST_TIMEOUT,
        )
        actual = r.stdout.strip()
        expected_clean = expected.strip()
        if r.returncode != 0:
            return {
                "status": "ERROR",
                "actual": actual[:1000],
                "expected": expected_clean[:1000],
                "stderr": r.stderr[:500],
                "exit_code": r.returncode,
            }
        # Tiered matching
        passed = (actual == expected_clean or
                  _normalize(actual) == _normalize(expected_clean) or
                  _floats_close(actual, expected_clean) or
                  _order_insensitive(_normalize(actual), _normalize(expected_clean)))
        return {
            "status": "PASS" if passed else "WRONG_OUTPUT",
            "actual": actual[:1000],
            "expected": expected_clean[:1000],
            "stderr": "",
            "exit_code": r.returncode,
        }
    except subprocess.TimeoutExpired:
        return {"status": "TIMEOUT", "actual": "", "expected": expected.strip()[:1000]}
    except Exception as e:
        return {"status": "ERROR", "actual": "", "expected": expected.strip()[:1000], "stderr": str(e)}


def process_one(req: dict) -> dict:
    req_id = req["id"]
    category = req["_category"]
    tc = req.get("test_cases", [{}])[0] if req.get("test_cases") else {}
    test_input = tc.get("input", "")
    expected = tc.get("expected_output", "")

    result = {"id": req_id, "category": category}
    out_dir = PYTHON_REFS_DIR / category / req_id
    out_dir.mkdir(parents=True, exist_ok=True)

    # Skip if already done
    status_file = out_dir / "status.json"
    if status_file.exists():
        with open(status_file) as f:
            existing = json.load(f)
        if existing.get("status") == "PASS":
            result["status"] = "SKIP_EXISTING"
            return result

    # Generate
    source = generate_python(req)
    if not source:
        result["status"] = "GEN_FAIL"
        return result

    # Save
    (out_dir / "solution.py").write_text(source)

    # Test
    test_result = test_python(source, test_input, expected)
    result.update(test_result)

    # Save output and status
    (out_dir / "output.txt").write_text(test_result.get("actual", ""))
    with open(status_file, "w") as f:
        json.dump({
            "status": test_result["status"],
            "actual": test_result.get("actual", "")[:500],
            "expected": expected[:500],
            "stderr": test_result.get("stderr", ""),
        }, f, indent=2)

    return result


def main():
    if not ANTHROPIC_API_KEY:
        print("ERROR: Set ANTHROPIC_API_KEY")
        sys.exit(1)

    print("Loading requirements...")
    reqs = load_requirements()
    print(f"Loaded {len(reqs)} requirements")

    PYTHON_REFS_DIR.mkdir(parents=True, exist_ok=True)

    results = []
    for batch_start in range(0, len(reqs), BATCH_SIZE):
        batch = reqs[batch_start:batch_start + BATCH_SIZE]
        batch_num = batch_start // BATCH_SIZE + 1
        total_batches = (len(reqs) + BATCH_SIZE - 1) // BATCH_SIZE
        print(f"Batch {batch_num}/{total_batches}: {[r['id'] for r in batch]}")

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {executor.submit(process_one, req): req["id"] for req in batch}
            for future in as_completed(futures):
                r = future.result()
                results.append(r)
                print(f"  {r['id']:10} → {r['status']}")

        time.sleep(0.5)

    # Summary
    from collections import Counter
    stats = Counter(r["status"] for r in results)
    print(f"\n=== RESULTS ({len(results)} programs) ===")
    for status, count in stats.most_common():
        pct = count / len(results) * 100
        print(f"  {status}: {count} ({pct:.1f}%)")

    # Save report
    with open(REPORT_PATH, "w") as f:
        json.dump({
            "total": len(results),
            "summary": dict(stats),
            "programs": results,
        }, f, indent=2)
    print(f"\nReport: {REPORT_PATH}")


if __name__ == "__main__":
    main()
