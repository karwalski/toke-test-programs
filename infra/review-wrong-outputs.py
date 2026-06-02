#!/usr/bin/env python3
"""review-wrong-outputs.py — Review programs where Python output differs completely from expected.

Uses Claude to analyse: requirement description + input + expected output + Python's actual output.
Determines if expected output is wrong and Python is correct. If so, updates the requirement YAML.

Output: results/output-review-report.json
"""

import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests
import yaml

BASE_DIR = Path(__file__).resolve().parent.parent
CATEGORIES_DIR = BASE_DIR / "categories"
PYTHON_REFS_DIR = BASE_DIR / "results" / "python-refs"
REPORT_PATH = BASE_DIR / "results" / "output-review-report.json"

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
MAX_WORKERS = 5
BATCH_SIZE = 10

REVIEW_PROMPT = """You are reviewing a test case for a programming exercise.

REQUIREMENT: {description}
INPUT FORMAT: {input_format}
INPUT: {test_input}
EXPECTED OUTPUT: {expected_output}
PYTHON'S ACTUAL OUTPUT: {python_output}

The Python program was asked to implement this requirement and produced a different output than expected.

Analyse:
1. Is the EXPECTED OUTPUT logically correct for the given requirement and input?
2. Is the PYTHON OUTPUT logically correct for the given requirement and input?
3. Which output is more plausible?

Respond with EXACTLY one of these JSON objects (no other text):
{{"verdict": "expected_correct", "reason": "brief reason"}}
{{"verdict": "python_correct", "reason": "brief reason", "correct_output": "the correct output"}}
{{"verdict": "both_wrong", "reason": "brief reason"}}
{{"verdict": "ambiguous", "reason": "brief reason"}}"""


def load_all_requirements() -> dict:
    reqs = {}
    for cat_dir in sorted(CATEGORIES_DIR.iterdir()):
        yf = cat_dir / "requirements.yaml"
        if not yf.exists():
            continue
        with open(yf) as f:
            items = yaml.safe_load(f)
        if items:
            for item in items:
                item["_category"] = cat_dir.name
                item["_yaml_path"] = str(yf)
                reqs[item["id"]] = item
    return reqs


def get_completely_different() -> list[dict]:
    """Find programs where Python output is completely different from expected."""
    programs = []
    for sf in PYTHON_REFS_DIR.rglob("status.json"):
        with open(sf) as f:
            d = json.load(f)
        if d["status"] != "WRONG_OUTPUT":
            continue
        actual = d.get("actual", "").strip()
        expected = d.get("expected", "").strip()
        if not actual:
            continue  # empty output handled separately
        # Skip if it's a near-match (float, whitespace, ordering)
        if expected in actual or actual in expected:
            continue
        programs.append({
            "id": sf.parent.name,
            "category": sf.parent.parent.name,
            "python_output": actual[:500],
            "expected": expected[:500],
        })
    return programs


def review_one(prog: dict, reqs: dict) -> dict:
    req = reqs.get(prog["id"])
    if not req:
        return {"id": prog["id"], "verdict": "no_requirement"}

    tc = req.get("test_cases", [{}])[0] if req.get("test_cases") else {}

    prompt = REVIEW_PROMPT.format(
        description=req.get("description", ""),
        input_format=req.get("input_format", ""),
        test_input=tc.get("input", "")[:300],
        expected_output=prog["expected"][:300],
        python_output=prog["python_output"][:300],
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
                "max_tokens": 512,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=60,
        )
        resp.raise_for_status()
        text = resp.json()["content"][0]["text"].strip()
        # Parse JSON from response
        m = re.search(r'\{[^}]+\}', text)
        if m:
            result = json.loads(m.group(0))
            result["id"] = prog["id"]
            result["category"] = prog["category"]
            return result
        return {"id": prog["id"], "verdict": "parse_error", "raw": text[:200]}
    except Exception as e:
        return {"id": prog["id"], "verdict": "api_error", "error": str(e)[:100]}


def main():
    if not ANTHROPIC_API_KEY:
        print("ERROR: Set ANTHROPIC_API_KEY")
        sys.exit(1)

    print("Loading requirements...")
    reqs = load_all_requirements()

    print("Finding completely different outputs...")
    programs = get_completely_different()
    print(f"Found {len(programs)} programs to review")

    results = []
    for batch_start in range(0, len(programs), BATCH_SIZE):
        batch = programs[batch_start:batch_start + BATCH_SIZE]
        batch_num = batch_start // BATCH_SIZE + 1
        total_batches = (len(programs) + BATCH_SIZE - 1) // BATCH_SIZE
        print(f"Batch {batch_num}/{total_batches}")

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {executor.submit(review_one, p, reqs): p["id"] for p in batch}
            for future in as_completed(futures):
                r = future.result()
                results.append(r)
                print(f"  {r['id']:10} → {r.get('verdict', '?')}")
        time.sleep(0.5)

    # Summary
    from collections import Counter
    verdicts = Counter(r.get("verdict") for r in results)
    print(f"\n=== REVIEW RESULTS ({len(results)} programs) ===")
    for v, c in verdicts.most_common():
        print(f"  {v}: {c}")

    # Save report
    with open(REPORT_PATH, "w") as f:
        json.dump({"total": len(results), "verdicts": dict(verdicts), "reviews": results}, f, indent=2)
    print(f"\nReport: {REPORT_PATH}")

    # Count programs where we should update expected output
    python_correct = [r for r in results if r.get("verdict") == "python_correct"]
    print(f"\nPrograms where Python is correct (update test cases): {len(python_correct)}")


if __name__ == "__main__":
    main()
