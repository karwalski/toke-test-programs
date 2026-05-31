#!/usr/bin/env python3
"""scan-trivial-prone-specs.py — flag specs whose test_cases are weak enough
that a hardcoded `io.println("constant")` would pass them.

Detects:
  1. All test_cases have IDENTICAL expected_output (single literal)
  2. All test_cases have SHORT expected_output (<20 chars) AND fewer than 3 test cases
  3. expected_output contains placeholder markers (<hex>, _hex, <sig>, etc.)
  4. expected_output is a single-word literal that's likely to appear naturally

These specs are vulnerable to trivial passes. R6 mitigation: either
  (a) add more diverse test cases, or
  (b) disable the spec until test_cases are hardened.

Output: results/spec-trivial-vulnerabilities.json + stdout summary.
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

BASE = Path(__file__).resolve().parent.parent
CATEGORIES = BASE / "categories"
OUT = BASE / "results" / "spec-trivial-vulnerabilities.json"


def is_placeholder(s: str) -> bool:
    if not s:
        return False
    if re.match(r"^<[\w_/]+>$", s.strip()):
        return True
    if s.endswith("_hex") or s.endswith("_placeholder") or s.endswith("_pub_hex"):
        return True
    if "<hex>" in s or "<sig>" in s or "<base64>" in s:
        return True
    return False


def main():
    vulnerabilities = []
    for req in sorted(CATEGORIES.glob("*/requirements.yaml")):
        cat = req.parent.name
        try:
            specs = yaml.safe_load(req.read_text())
        except Exception:
            continue
        for spec in specs or []:
            pid = spec.get("id")
            if not pid:
                continue
            if spec.get("disabled"):
                continue  # already disabled
            tcs = spec.get("test_cases", [])
            if not tcs:
                continue

            issues = []
            exp_vals = [(t.get("expected_output", "") or "").strip() for t in tcs]
            uniq_exp = set(exp_vals)

            # (1) all identical
            if len(uniq_exp) == 1 and len(tcs) >= 2:
                v = next(iter(uniq_exp))
                if len(v) < 50:
                    issues.append(f"ALL_TESTS_SAME_OUTPUT (n={len(tcs)}): {v!r}")

            # (2) Only flag SHORT outputs when they're identical OR are sentinel/non-computed.
            # Different numerical outputs per test = model must read input + compute, not trivially cheatable.
            # (Removed the broad SHORT_OUTPUTS_FEW_TESTS check — was over-flagging legitimate
            # finance/math specs where the outputs are distinct computed values.)

            # (3) placeholder markers
            for i, v in enumerate(exp_vals):
                if is_placeholder(v):
                    issues.append(f"PLACEHOLDER in test_{i+1}: {v!r}")

            # (4) Single-word literal (no whitespace, alphanum only) — high cheat risk
            for i, v in enumerate(exp_vals):
                if v and re.match(r"^[A-Za-z0-9_]{2,20}$", v):
                    # Common indicator words are particularly weak
                    if v.upper() in {"PASS", "FAIL", "OK", "YES", "NO", "TRUE", "FALSE",
                                      "VALID", "INVALID", "ALLOW", "DENY", "PERMIT",
                                      "SUCCESS", "ERROR", "SENT", "RECEIVED", "SERVING",
                                      "ACTIVE", "INACTIVE", "REPLAYING"}:
                        issues.append(f"SENTINEL_OUTPUT in test_{i+1}: {v!r}")

            if issues:
                vulnerabilities.append({
                    "id": pid, "category": cat, "n_test_cases": len(tcs),
                    "issues": issues, "expected_outputs": exp_vals[:3],
                })

    # Aggregate
    by_cat = Counter(v["category"] for v in vulnerabilities)
    by_issue = Counter()
    for v in vulnerabilities:
        for i in v["issues"]:
            by_issue[i.split(":")[0].split(" ")[0]] += 1

    print(f"Scanned {sum(1 for _ in CATEGORIES.glob('*/requirements.yaml'))} category files")
    print(f"Specs with trivial-pass vulnerabilities: {len(vulnerabilities)}")
    print()
    print("=== By issue type ===")
    for k, n in by_issue.most_common():
        print(f"  {n:4d}  {k}")
    print()
    print("=== Top 5 categories ===")
    for cat, n in by_cat.most_common(5):
        print(f"  {n:3d}  {cat}")
    print()
    print("=== First 15 vulnerable specs ===")
    for v in vulnerabilities[:15]:
        print(f"  {v['id']:<10} [{v['category']:<20}] {v['issues'][0]}")
    if len(vulnerabilities) > 15:
        print(f"  ... and {len(vulnerabilities) - 15} more")

    OUT.write_text(json.dumps({"total": len(vulnerabilities),
                                "by_category": dict(by_cat),
                                "by_issue_type": dict(by_issue),
                                "vulnerabilities": vulnerabilities}, indent=2))
    print(f"\nFull: {OUT}")


if __name__ == "__main__":
    main()
