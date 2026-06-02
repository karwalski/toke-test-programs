#!/usr/bin/env python3
"""fix-python-batch.py — Fix Python reference programs that have known issues.

For extra_output: trim the Python code to only print what's expected.
For empty_output: regenerate with stronger print emphasis.
For error_in_stdout: fix the runtime error.

Usage:
    ANTHROPIC_API_KEY=... python3 fix-python-batch.py <category> [--dry-run]

Categories: extra_output, empty_output, error_in_stdout, all
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
CATEGORIES_DIR = BASE_DIR / "categories"
PYTHON_REFS_DIR = BASE_DIR / "results" / "python-refs"
QUICKWINS_FILE = Path("/tmp/python_quickwins.json")

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
TEST_TIMEOUT = 10
MAX_WORKERS = 5


def _normalize(s):
    s = s.strip()
    s = re.sub(r'[ \t]+', ' ', s)
    s = s.replace('\r\n', '\n').replace('\r', '\n')
    s = '\n'.join(line.rstrip() for line in s.split('\n'))
    return s


def _floats_close(actual, expected, rel_tol=0.01):
    a_nums = re.findall(r'-?\d+\.?\d*(?:[eE][+-]?\d+)?', actual)
    e_nums = re.findall(r'-?\d+\.?\d*(?:[eE][+-]?\d+)?', expected)
    if not a_nums or not e_nums or len(a_nums) != len(e_nums):
        return False
    try:
        for a, e in zip(a_nums, e_nums):
            af, ef = float(a), float(e)
            if ef == 0:
                if abs(af) > 0.001: return False
            elif abs(af - ef) / max(abs(ef), 1e-9) > rel_tol: return False
        a_text = re.sub(r'-?\d+\.?\d*(?:[eE][+-]?\d+)?', '#', actual)
        e_text = re.sub(r'-?\d+\.?\d*(?:[eE][+-]?\d+)?', '#', expected)
        if _normalize(a_text) != _normalize(e_text): return False
        return True
    except:
        return False


def passes(actual, expected):
    a, e = actual.strip(), expected.strip()
    return (a == e or _normalize(a) == _normalize(e) or
            _floats_close(a, e) or
            sorted(a.split()) == sorted(e.split()) and len(a.split()) > 1)


def load_requirement(prog_id):
    for cat_dir in CATEGORIES_DIR.iterdir():
        yf = cat_dir / "requirements.yaml"
        if not yf.exists():
            continue
        with open(yf) as f:
            items = yaml.safe_load(f)
        if items:
            for item in items:
                if item["id"] == prog_id:
                    return item
    return None


def call_claude(prompt):
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


def test_python(source, test_input, expected):
    try:
        r = subprocess.run(
            [sys.executable, "-c", source],
            input=test_input, capture_output=True, text=True, timeout=TEST_TIMEOUT,
        )
        actual = r.stdout.strip()
        if r.returncode != 0:
            return "ERROR", actual, r.stderr[:300]
        if passes(actual, expected):
            return "PASS", actual, ""
        return "WRONG_OUTPUT", actual, ""
    except subprocess.TimeoutExpired:
        return "TIMEOUT", "", ""


def fix_extra_output(prog_id):
    """Python prints too much — ask Claude to trim."""
    ref_dir = None
    for cat_dir in PYTHON_REFS_DIR.iterdir():
        candidate = cat_dir / prog_id
        if candidate.exists():
            ref_dir = candidate
            break
    if not ref_dir:
        return {"id": prog_id, "status": "NOT_FOUND"}

    source = (ref_dir / "solution.py").read_text()
    with open(ref_dir / "status.json") as f:
        status = json.load(f)

    req = load_requirement(prog_id)
    tc = req.get("test_cases", [{}])[0] if req and req.get("test_cases") else {}

    prompt = f"""Fix this Python program. It produces EXTRA output beyond what's expected.

EXPECTED OUTPUT (exact):
{status.get('expected', '')[:500]}

ACTUAL OUTPUT (too much):
{status.get('actual', '')[:500]}

CURRENT CODE:
```python
{source}
```

The program prints extra headers, labels, or debug info not in the expected output.
Remove any extra print statements. Output must EXACTLY match the expected output.
Use ONLY Python standard library. Must complete in <10 seconds.

Return ONLY the fixed Python code in ```python``` markers."""

    fixed = call_claude(prompt)
    if not fixed:
        return {"id": prog_id, "status": "API_FAIL"}

    test_input = tc.get("input", "")
    expected = tc.get("expected_output", "")
    result_status, actual, err = test_python(fixed, test_input, expected)

    if result_status == "PASS":
        (ref_dir / "solution.py").write_text(fixed)
        (ref_dir / "output.txt").write_text(actual)
        with open(ref_dir / "status.json", "w") as f:
            json.dump({"status": "PASS", "actual": actual[:500], "expected": expected[:500]}, f, indent=2)

    return {"id": prog_id, "status": result_status}


def fix_empty_output(prog_id):
    """Python prints nothing — regenerate with emphasis on printing."""
    req = load_requirement(prog_id)
    if not req:
        return {"id": prog_id, "status": "NO_REQ"}

    tc = req.get("test_cases", [{}])[0] if req.get("test_cases") else {}

    prompt = f"""Write a Python 3 program that solves this requirement.

REQUIREMENT: {req.get('description', '')}
INPUT FORMAT: {req.get('input_format', '')}
OUTPUT FORMAT: {req.get('output_format', '')}
TEST INPUT: {tc.get('input', '')[:500]}
EXPECTED OUTPUT: {tc.get('expected_output', '')[:500]}

CRITICAL: The program MUST print output to stdout using print().
The output must EXACTLY match the expected output above.
Read input from stdin. Use ONLY Python 3 standard library.
NO pip packages. Must complete in <10 seconds. NO servers, NO infinite loops.

Return ONLY the Python code in ```python``` markers."""

    fixed = call_claude(prompt)
    if not fixed:
        return {"id": prog_id, "status": "API_FAIL"}

    result_status, actual, err = test_python(fixed, tc.get("input", ""), tc.get("expected_output", ""))

    ref_dir = None
    for cat_dir in PYTHON_REFS_DIR.iterdir():
        candidate = cat_dir / prog_id
        if candidate.exists():
            ref_dir = candidate
            break
    if not ref_dir:
        # Create it
        cat = req.get("_category", "unknown")
        ref_dir = PYTHON_REFS_DIR / cat / prog_id
        ref_dir.mkdir(parents=True, exist_ok=True)

    (ref_dir / "solution.py").write_text(fixed)
    (ref_dir / "output.txt").write_text(actual)
    with open(ref_dir / "status.json", "w") as f:
        json.dump({"status": result_status, "actual": actual[:500],
                    "expected": tc.get("expected_output", "")[:500],
                    "stderr": err[:300]}, f, indent=2)

    return {"id": prog_id, "status": result_status}


def fix_error_in_stdout(prog_id):
    """Python has runtime error — same as empty_output, regenerate."""
    return fix_empty_output(prog_id)


def main():
    if not ANTHROPIC_API_KEY:
        print("ERROR: Set ANTHROPIC_API_KEY")
        sys.exit(1)

    category = sys.argv[1] if len(sys.argv) > 1 else "all"

    with open(QUICKWINS_FILE) as f:
        quickwins = json.load(f)

    if category == "all":
        programs = [(pid, fix_extra_output) for pid in quickwins["extra_output"]]
        programs += [(pid, fix_empty_output) for pid in quickwins["empty_output"]]
        programs += [(pid, fix_error_in_stdout) for pid in quickwins["error_in_stdout"]]
    elif category == "extra_output":
        programs = [(pid, fix_extra_output) for pid in quickwins["extra_output"]]
    elif category == "empty_output":
        programs = [(pid, fix_empty_output) for pid in quickwins["empty_output"]]
    elif category == "error_in_stdout":
        programs = [(pid, fix_error_in_stdout) for pid in quickwins["error_in_stdout"]]
    else:
        print(f"Unknown category: {category}")
        sys.exit(1)

    print(f"Processing {len(programs)} programs ({category})...")

    results = []
    batch_size = 10
    for batch_start in range(0, len(programs), batch_size):
        batch = programs[batch_start:batch_start + batch_size]
        batch_num = batch_start // batch_size + 1
        total_batches = (len(programs) + batch_size - 1) // batch_size
        print(f"Batch {batch_num}/{total_batches}")

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {executor.submit(fn, pid): pid for pid, fn in batch}
            for future in as_completed(futures):
                r = future.result()
                results.append(r)
                print(f"  {r['id']:10} → {r['status']}")
        time.sleep(0.5)

    from collections import Counter
    stats = Counter(r["status"] for r in results)
    print(f"\n=== RESULTS ===")
    for s, c in stats.most_common():
        print(f"  {s}: {c}")


if __name__ == "__main__":
    main()
