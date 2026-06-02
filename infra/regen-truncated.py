#!/usr/bin/env python3
"""regen-truncated.py — Regenerate truncated toke programs with higher token limit.

Calls the toke API for each program, only overwrites if the new code is better
(longer, compiles, or at least has more valid syntax).
"""

import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import requests
import yaml

BASE_DIR = Path(__file__).resolve().parent.parent
CATEGORIES_DIR = BASE_DIR / "categories"
SOLUTIONS_DIR = BASE_DIR / "results" / "solutions"
REGEN_LIST = Path(os.environ.get("REGEN_LIST", "/tmp/regen_truncated.json"))

TOKE_API_URL = os.environ.get("TOKE_API_URL", "https://api.tokelang.dev")
TOKE_API_KEY = os.environ.get("TOKE_API_KEY", "")
TKC = "tkc"
TKC_TIMEOUT = 60
TEST_TIMEOUT = 10


def load_requirements() -> dict:
    reqs = {}
    for cat_dir in sorted(CATEGORIES_DIR.iterdir()):
        yf = cat_dir / "requirements.yaml"
        if not yf.exists():
            continue
        with open(yf) as f:
            items = yaml.safe_load(f)
        if items:
            for item in items:
                reqs[item["id"]] = item
    return reqs


def call_toke_api(description: str, req: dict) -> str | None:
    try:
        resp = requests.post(
            f"{TOKE_API_URL}/v1/generate",
            headers={
                "X-Api-Key": TOKE_API_KEY,
                "Content-Type": "application/json",
            },
            json={
                "description": description,
                "difficulty": req.get("difficulty", 2),
                "stdlib_modules": req.get("stdlib_modules", []),
                "input_format": req.get("input_format", ""),
                "output_format": req.get("output_format", ""),
                "max_tokens": 2048,
            },
            timeout=120,
        )
        resp.raise_for_status()
        data = resp.json()
        return data.get("code") or data.get("source")
    except Exception as e:
        print(f"    API error: {e}")
        return None


def check_compiles(source: str) -> tuple[bool, str]:
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".tk", mode="w", delete=False) as f:
        f.write(source)
        f.flush()
        try:
            r = subprocess.run([TKC, "--check", f.name],
                             capture_output=True, text=True, timeout=TKC_TIMEOUT)
            return r.returncode == 0, (r.stdout + r.stderr).strip()
        except:
            return False, "timeout"
        finally:
            os.unlink(f.name)


def check_builds_and_runs(source: str, req: dict) -> tuple[str, str]:
    """Returns (status, detail)"""
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        src = Path(tmpdir) / "prog.tk"
        binary = Path(tmpdir) / "prog"
        src.write_text(source)

        r = subprocess.run([TKC, "--check", str(src)],
                          capture_output=True, text=True, timeout=TKC_TIMEOUT)
        if r.returncode != 0:
            return "COMPILE_FAIL", (r.stdout + r.stderr)[:200]

        r = subprocess.run([TKC, "--out", str(binary), str(src)],
                          capture_output=True, text=True, timeout=TKC_TIMEOUT)
        if r.returncode != 0 or not binary.exists():
            return "BUILD_FAIL", (r.stdout + r.stderr)[:200]

        tc = req.get("test_cases", [{}])[0] if req.get("test_cases") else {}
        try:
            r = subprocess.run([str(binary)], input=tc.get("input", ""),
                             capture_output=True, text=True, timeout=TEST_TIMEOUT)
            actual = r.stdout.strip()
            expected = tc.get("expected_output", "").strip()
            if r.returncode == -11:
                return "SEGFAULT", ""
            if actual == expected:
                return "PASS", actual
            return "WRONG_OUTPUT", actual[:100]
        except subprocess.TimeoutExpired:
            return "TIMEOUT", ""


def main():
    if not TOKE_API_KEY:
        print("ERROR: Set TOKE_API_KEY")
        sys.exit(1)

    with open(REGEN_LIST) as f:
        programs = json.load(f)

    reqs = load_requirements()
    print(f"Regenerating {len(programs)} truncated programs...\n")

    stats = {"regenerated": 0, "improved": 0, "same_or_worse": 0,
             "api_fail": 0, "compiles": 0, "passes": 0}

    for i, prog in enumerate(programs):
        pid = prog["id"]
        cat = prog["category"]
        old_hash = prog["source_hash"]
        old_bytes = prog["source_bytes"]

        req = reqs.get(pid)
        if not req:
            continue

        print(f"[{i+1}/{len(programs)}] {pid} ({old_bytes}b)...", end=" ", flush=True)

        # Call toke API
        new_source = call_toke_api(req.get("description", ""), req)
        if not new_source:
            stats["api_fail"] += 1
            print("API fail")
            continue

        new_hash = hashlib.sha256(new_source.encode()).hexdigest()[:16]
        new_bytes = len(new_source)

        # Is it actually longer/different?
        if new_bytes <= old_bytes:
            stats["same_or_worse"] += 1
            print(f"no improvement ({new_bytes}b <= {old_bytes}b)")
            continue

        # Check if new version compiles
        compiles, _ = check_compiles(new_source)
        if compiles:
            stats["compiles"] += 1

        # Full test
        status, detail = check_builds_and_runs(new_source, req)

        # Save if improved (longer, or compiles when old didn't)
        sol_dir = None
        for cat_dir in SOLUTIONS_DIR.iterdir():
            candidate = cat_dir / pid
            if candidate.exists():
                sol_dir = candidate
                break

        if sol_dir:
            # Verify old source hash matches — don't overwrite if someone else changed it
            old_source = (sol_dir / "solution.tk").read_text()
            current_hash = hashlib.sha256(old_source.encode()).hexdigest()[:16]
            if current_hash != old_hash:
                print(f"SKIP (source changed since audit)")
                continue

            (sol_dir / "solution.tk").write_text(new_source)
            stats["regenerated"] += 1
            if status == "PASS":
                stats["passes"] += 1

            print(f"{old_bytes}b → {new_bytes}b  {status}")
        else:
            print(f"no solution dir found")

        time.sleep(0.5)  # rate limit

    print(f"\n=== RESULTS ===")
    for k, v in stats.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
