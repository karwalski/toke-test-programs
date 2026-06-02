#!/usr/bin/env python3
"""fix-python-errors.py — Fix Python programs that error, grouped by error type.

Each group gets a targeted prompt explaining the specific issue.
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
CLASSIFICATION_FILE = BASE_DIR / "results" / "python-error-classification.json"

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
TEST_TIMEOUT = 10
MAX_WORKERS = 5

GROUP_PROMPTS = {
    "ValueError_hex": """Fix this Python program. It crashes because it uses PLACEHOLDER variable names
as hex strings (e.g. "private_d_hex" passed to bytes.fromhex()).

You must generate ACTUAL hex values for the crypto operations. Use hashlib, hmac, secrets
from stdlib to generate real test data. Do NOT use placeholder strings.
For private keys, use secrets.token_hex(32). For hashes, use hashlib.sha256().
For ECDSA/Ed25519 — implement a simplified version or use fixed known test vectors.""",

    "ModuleNotFoundError": """Fix this Python program. It imports a non-stdlib package that isn't available.
Rewrite using ONLY Python 3 standard library. Common replacements:
- cryptography/Crypto/Cryptodome → hashlib, hmac, secrets, struct
- psutil → subprocess + parsing /proc or os module
- websockets → socket module
- requests → urllib.request
Do NOT import any pip packages.""",

    "EOFError_stdin": """Fix this Python program. It crashes with EOFError because it calls input()
but may receive no interactive input. The program reads from stdin.
Use sys.stdin.read() or try/except around input() calls.
If the program needs specific input, read it from stdin (it will be piped in).""",

    "FileNotFoundError": """Fix this Python program. It crashes because it accesses files that don't exist
(e.g. /proc/* paths on non-Linux systems, or temp files).
Make the program work without relying on specific filesystem paths.
Use os.path.exists() checks, or generate the data in-memory instead of reading files.""",

    "IndexError": """Fix this Python program. It crashes with IndexError — accessing list/string
index out of range. Add bounds checking before indexing.
Check len() before accessing indices. Use try/except if needed.""",

    "SyntaxError": """Fix this Python program. It has a syntax error — likely from incomplete code generation.
Rewrite the program completely from the requirement.""",

    "ValueError_base64": """Fix this Python program. It crashes on base64.b64decode with invalid input.
Use actual base64-encoded test data instead of placeholder strings.
Generate real base64 values using base64.b64encode(data).""",

    "ValueError_other": """Fix this Python program. It crashes with a ValueError during type conversion or parsing.
Check input validation, add try/except for conversions, handle edge cases.""",

    "TIMEOUT": """Fix this Python program. It times out (takes >10 seconds).
The program must NOT start a server, open sockets, or run infinite loops.
Simulate the behavior: process the input, compute the expected output, print it, and exit.
For server programs: print what the server WOULD respond, don't actually listen.
For game loops: run a fixed number of iterations based on input, don't loop forever.""",

    "Other": """Fix this Python program. It has a runtime error.
Review the traceback, fix the bug, and ensure it produces the expected output.""",
}


def _normalize(s):
    s = s.strip()
    s = re.sub(r'[ \t]+', ' ', s)
    s = s.replace('\r\n', '\n').replace('\r', '\n')
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
        a_text = re.sub(r'-?\d+\.?\d*(?:[eE][+-]?\d+)?', '#', actual)
        e_text = re.sub(r'-?\d+\.?\d*(?:[eE][+-]?\d+)?', '#', expected)
        if _normalize(a_text) != _normalize(e_text): return False
        return True
    except: return False

def passes(actual, expected):
    a, e = actual.strip(), expected.strip()
    return (a == e or _normalize(a) == _normalize(e) or _floats_close(a, e) or
            (sorted(a.split()) == sorted(e.split()) and len(a.split()) > 1))


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


def fix_program(prog_id, group, group_prompt):
    ref_dir = find_ref_dir(prog_id)
    req = load_requirement(prog_id)
    if not ref_dir or not req:
        return {"id": prog_id, "status": "NOT_FOUND"}

    source = (ref_dir / "solution.py").read_text() if (ref_dir / "solution.py").exists() else ""
    with open(ref_dir / "status.json") as f:
        status_data = json.load(f)

    tc = req.get("test_cases", [{}])[0] if req.get("test_cases") else {}

    prompt = f"""{group_prompt}

REQUIREMENT: {req.get('description', '')}
INPUT FORMAT: {req.get('input_format', '')}
TEST INPUT: {tc.get('input', '')[:300]}
EXPECTED OUTPUT: {tc.get('expected_output', '')[:300]}

CURRENT CODE (has error):
```python
{source[:2000]}
```

ERROR:
{status_data.get('stderr', '')[:500]}

Rules:
- Use ONLY Python 3 standard library
- Read from stdin, write to stdout
- Must complete in <10 seconds
- Output must EXACTLY match expected output

Return ONLY the fixed Python code in ```python``` markers."""

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
    except Exception:
        return {"id": prog_id, "status": "API_FAIL"}

    # Test
    try:
        r = subprocess.run(
            [sys.executable, "-c", fixed],
            input=tc.get("input", ""), capture_output=True, text=True, timeout=TEST_TIMEOUT,
        )
        actual = r.stdout.strip()
        expected = tc.get("expected_output", "").strip()
        if r.returncode != 0:
            result_status = "ERROR"
        elif passes(actual, expected):
            result_status = "PASS"
        else:
            result_status = "WRONG_OUTPUT"
    except subprocess.TimeoutExpired:
        result_status = "TIMEOUT"
        actual = ""
    except Exception:
        result_status = "ERROR"
        actual = ""

    # Save if improved
    if result_status in ("PASS", "WRONG_OUTPUT"):
        (ref_dir / "solution.py").write_text(fixed)
        (ref_dir / "output.txt").write_text(actual)
        with open(ref_dir / "status.json", "w") as f:
            json.dump({"status": result_status, "actual": actual[:500],
                       "expected": expected[:500]}, f, indent=2)

    return {"id": prog_id, "group": group, "status": result_status}


def main():
    if not ANTHROPIC_API_KEY:
        print("ERROR: Set ANTHROPIC_API_KEY")
        sys.exit(1)

    with open(CLASSIFICATION_FILE) as f:
        classification = json.load(f)

    results = []
    for group, info in classification["groups"].items():
        pids = info["program_ids"]
        prompt = GROUP_PROMPTS.get(group, GROUP_PROMPTS["Other"])
        print(f"\n=== {group}: {len(pids)} programs ===")

        for batch_start in range(0, len(pids), 10):
            batch = pids[batch_start:batch_start + 10]
            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                futures = {executor.submit(fix_program, pid, group, prompt): pid for pid in batch}
                for future in as_completed(futures):
                    r = future.result()
                    results.append(r)
                    print(f"  {r['id']:10} → {r['status']}")
            time.sleep(0.5)

    from collections import Counter
    stats = Counter(r["status"] for r in results)
    print(f"\n=== TOTAL RESULTS ({len(results)}) ===")
    for s, c in stats.most_common():
        print(f"  {s}: {c}")

    # Per-group results
    print("\n=== PER GROUP ===")
    group_stats = {}
    for r in results:
        g = r.get("group", "?")
        if g not in group_stats:
            group_stats[g] = Counter()
        group_stats[g][r["status"]] += 1
    for g, stats in sorted(group_stats.items()):
        print(f"  {g}: {dict(stats)}")


if __name__ == "__main__":
    main()
