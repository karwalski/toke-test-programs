#!/usr/bin/env python3
"""apply-107-R7-disables.py — disable 174 specs with weak test_cases.

Reads results/spec-trivial-vulnerabilities.json from scan-trivial-prone-specs.py
and disables every spec flagged with:
  - ALL_TESTS_SAME_OUTPUT (156): all test cases expect the same literal
  - PLACEHOLDER (18): literal <hex>/<sig>/_hex in expected_output

SENTINEL_OUTPUT specs are KEPT — they can pass legitimately when the model
implements the actual classifier. They'll be reviewed case-by-case in R8.

Line-level edit preserves YAML formatting. Idempotent.
"""

import json
import re
import sys
from datetime import date
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
CATEGORIES = BASE / "categories"
VULNS = BASE / "results" / "spec-trivial-vulnerabilities.json"

DISABLE_ISSUE_TYPES = {"ALL_TESTS_SAME_OUTPUT", "PLACEHOLDER"}


def disable_in_file(req_path: Path, target_id: str, reason: str, today: str) -> bool:
    text = req_path.read_text()
    lines = text.split("\n")
    out = []
    i = 0
    edited = False
    while i < len(lines):
        line = lines[i]
        out.append(line)
        m = re.match(r'^- id:\s*["\']?([A-Z]+-\d+)["\']?\s*$', line)
        if m and m.group(1) == target_id:
            if i + 1 < len(lines) and re.match(r'^\s+disabled:\s*true\b', lines[i + 1]):
                pass  # already disabled
            else:
                esc = reason.replace('\\', '\\\\').replace('"', "'")
                out.append('  disabled: true')
                out.append(f'  disabled_reason: "{esc}"')
                out.append(f'  disabled_at: "{today}"')
                out.append('  disabled_by: "107-R7-trivial-test-cases"')
                edited = True
        i += 1
    if edited:
        req_path.write_text("\n".join(out))
    return edited


def main():
    if not VULNS.exists():
        print(f"missing {VULNS} — run scan-trivial-prone-specs.py first", file=sys.stderr)
        sys.exit(1)
    data = json.loads(VULNS.read_text())
    today = date.today().isoformat()

    targets: dict[str, dict] = {}  # id -> {category, reason}
    for v in data["vulnerabilities"]:
        issue_types = {i.split(":")[0].split(" ")[0] for i in v["issues"]}
        if issue_types & DISABLE_ISSUE_TYPES:
            primary_issue = next(iter(issue_types & DISABLE_ISSUE_TYPES))
            sample = v["expected_outputs"][0] if v["expected_outputs"] else "?"
            reason = f"[{primary_issue}] test_cases admit trivially-hardcoded constants. Expected sample: {sample[:80]!r}"
            targets[v["id"]] = {"category": v["category"], "reason": reason}

    print(f"Targets to disable: {len(targets)}")
    by_cat: dict[str, int] = {}
    skipped_already = 0
    disabled_now = 0

    for pid, info in targets.items():
        cat = info["category"]
        req = CATEGORIES / cat / "requirements.yaml"
        if not req.exists():
            print(f"WARN: {req} not found", file=sys.stderr)
            continue
        if disable_in_file(req, pid, info["reason"], today):
            disabled_now += 1
            by_cat[cat] = by_cat.get(cat, 0) + 1
        else:
            skipped_already += 1

    print(f"\nDisabled now: {disabled_now}")
    print(f"Already disabled (no-op): {skipped_already}")
    print(f"\nPer category:")
    for cat in sorted(by_cat, key=lambda c: -by_cat[c]):
        print(f"  {cat:<22} {by_cat[cat]:>4}")


if __name__ == "__main__":
    main()
