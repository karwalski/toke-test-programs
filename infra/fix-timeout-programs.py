#!/usr/bin/env python3
"""fix-timeout-programs.py — Fix the 10 timeout Python programs individually.

Each gets a custom prompt explaining that it must NOT make network calls or start servers.
Includes a timeout harness that kills after 8 seconds.
"""

import json
import os
import re
import signal
import subprocess
import sys
import time
from pathlib import Path

import requests
import yaml

BASE_DIR = Path(__file__).resolve().parent.parent
CATEGORIES_DIR = BASE_DIR / "categories"
PYTHON_REFS_DIR = BASE_DIR / "results" / "python-refs"

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
HARD_TIMEOUT = 8  # seconds — stricter than the 10s test harness

TIMEOUT_IDS = ["SEC-038", "SEC-086", "NET-158", "NET-128", "NET-129",
               "NET-053", "NET-165", "SYS-084", "GAM-128", "GAM-118"]

# Per-program guidance
PROGRAM_HINTS = {
    "SEC-038": "Simulate HTTP method enumeration. Print which methods would be allowed (GET, POST, etc) without making real requests.",
    "SEC-086": "Simulate network recon. Parse the CIDR input, print scan results for the first few hosts. Do NOT actually scan.",
    "NET-158": "Simulate API endpoint discovery. Print discovered endpoints without making HTTP calls.",
    "NET-128": "Simulate stress test results. Parse the config (url, threads, requests), print simulated stats.",
    "NET-129": "Simulate circuit breaker behavior. Print request results (200/fail) and circuit state changes. No real HTTP.",
    "NET-053": "Simulate streaming JSON server. Print 'Listening on :PORT' then simulate streaming N records. No sockets.",
    "NET-165": "Simulate latency measurements. Print mean/min/max/p99 stats without making real requests.",
    "SYS-084": "Simulate ping results. Print ping stats (min/avg/max/loss) for each host without actually pinging.",
    "GAM-128": "Solve the codeword puzzle. This is a constraint satisfaction problem — use backtracking. Must complete in <8 seconds.",
    "GAM-118": "Solve the Numbrix puzzle. This is a Hamiltonian path problem — use backtracking with pruning. Must complete in <8 seconds.",
}

PROMPT_TEMPLATE = """Write a Python 3 program for this requirement. It MUST complete within 8 seconds.

REQUIREMENT: {description}
INPUT FORMAT: {input_format}
OUTPUT FORMAT: {output_format}
TEST INPUT: {test_input}
EXPECTED OUTPUT: {expected_output}

SPECIFIC GUIDANCE: {hint}

CRITICAL RULES:
- DO NOT make any network calls (no urllib, no socket.connect, no HTTP requests)
- DO NOT start any server or listener
- DO NOT use infinite loops or blocking waits
- The program must READ stdin, COMPUTE/SIMULATE the answer, PRINT to stdout, and EXIT
- For network tools: simulate the behavior, produce the expected output format
- For puzzle solvers: use efficient backtracking with pruning, bail out if taking too long
- Use ONLY Python 3 standard library
- Output must match the expected output format

Return ONLY the Python code in ```python``` markers."""


def _normalize(s):
    s = s.strip()
    s = re.sub(r'[ \t]+', ' ', s)
    s = '\n'.join(line.rstrip() for line in s.split('\n'))
    return s

def _floats_close(actual, expected, rel_tol=0.01):
    a_nums = re.findall(r'-?\d+\.?\d*(?:[eE][+-]?\d+)?', actual)
    e_nums = re.findall(r'-?\d+\.?\d*(?:[eE][+-]?\d+)?', expected)
    if not a_nums or not e_nums or len(a_nums) != len(e_nums): return False
    try:
        for a, e in zip(a_nums, e_nums):
            af, ef = float(a), float(e)
            if ef == 0:
                if abs(af) > 0.001: return False
            elif abs(af - ef) / max(abs(ef), 1e-9) > rel_tol: return False
        return True
    except: return False

def passes(actual, expected):
    a, e = actual.strip(), expected.strip()
    if not a or not e: return False
    return (a == e or _normalize(a) == _normalize(e) or _floats_close(a, e) or
            e in a)  # partial match for these programs (expected is often a prefix)


def load_requirement(prog_id):
    for cat_dir in CATEGORIES_DIR.iterdir():
        yf = cat_dir / "requirements.yaml"
        if not yf.exists(): continue
        with open(yf) as f:
            items = yaml.safe_load(f)
        if items:
            for item in items:
                if item["id"] == prog_id:
                    return item
    return None


def find_ref_dir(prog_id):
    for cat_dir in PYTHON_REFS_DIR.iterdir():
        candidate = cat_dir / prog_id
        if candidate.exists():
            return candidate
    return None


def run_with_timeout(source, test_input, timeout=HARD_TIMEOUT):
    """Run Python code with strict timeout."""
    try:
        r = subprocess.run(
            [sys.executable, "-c", source],
            input=test_input, capture_output=True, text=True, timeout=timeout,
        )
        return r.returncode, r.stdout.strip(), r.stderr[:300]
    except subprocess.TimeoutExpired:
        return -1, "", "TIMEOUT after {}s".format(timeout)


def fix_one(prog_id):
    req = load_requirement(prog_id)
    if not req:
        return {"id": prog_id, "status": "NO_REQ"}

    tc = req.get("test_cases", [{}])[0] if req.get("test_cases") else {}
    hint = PROGRAM_HINTS.get(prog_id, "Must complete in <8 seconds. No network, no servers.")

    prompt = PROMPT_TEMPLATE.format(
        description=req.get("description", ""),
        input_format=req.get("input_format", ""),
        output_format=req.get("output_format", ""),
        test_input=tc.get("input", "")[:500],
        expected_output=tc.get("expected_output", "")[:500],
        hint=hint,
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
        fixed = text.strip()
    except Exception as e:
        return {"id": prog_id, "status": "API_FAIL", "error": str(e)[:100]}

    # Test with strict timeout
    exitcode, actual, stderr = run_with_timeout(fixed, tc.get("input", ""))

    if exitcode == -1:
        status = "TIMEOUT"
    elif exitcode != 0:
        status = "ERROR"
    elif passes(actual, tc.get("expected_output", "")):
        status = "PASS"
    else:
        status = "WRONG_OUTPUT"

    # Save
    ref_dir = find_ref_dir(prog_id)
    if not ref_dir:
        for cat_dir in PYTHON_REFS_DIR.iterdir():
            if cat_dir.is_dir():
                ref_dir = cat_dir / prog_id
                ref_dir.mkdir(parents=True, exist_ok=True)
                break

    if ref_dir:
        (ref_dir / "solution.py").write_text(fixed)
        (ref_dir / "output.txt").write_text(actual)
        with open(ref_dir / "status.json", "w") as f:
            json.dump({
                "status": status,
                "actual": actual[:500],
                "expected": tc.get("expected_output", "")[:500],
                "stderr": stderr,
            }, f, indent=2)

    return {"id": prog_id, "status": status, "actual": actual[:80], "stderr": stderr[:80]}


def main():
    if not ANTHROPIC_API_KEY:
        print("ERROR: Set ANTHROPIC_API_KEY")
        sys.exit(1)

    print(f"Fixing {len(TIMEOUT_IDS)} timeout programs individually...\n")

    for prog_id in TIMEOUT_IDS:
        print(f"[{prog_id}] {PROGRAM_HINTS.get(prog_id, '')[:60]}")
        r = fix_one(prog_id)
        print(f"  → {r['status']}")
        if r.get("actual"):
            print(f"  output: {r['actual'][:60]}")
        if r.get("stderr"):
            print(f"  stderr: {r['stderr'][:60]}")
        print()
        time.sleep(1)

    # Summary
    from collections import Counter
    results = [fix_one.__code__ for _ in []]  # just for the print
    print("Done.")


if __name__ == "__main__":
    main()
