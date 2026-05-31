#!/usr/bin/env python3
"""review-107-R5-fails.py — categorize all 55 R5 fails + surface patterns.

For each failed program:
  - Pull last-attempt.tk + error.log from results/107-R5/failed/<cat>/<id>/
  - Re-test with local tkc via toke_test_harness.classify_failure
  - Bucket by failure mode + collect error codes
  - Cross-reference spec for placeholder-output / requires-network / requires-llm

Surface: top error codes, missing-print issues, broken-spec issues, new failure
modes not seen in 107.R3 categorisation.
"""

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent))
from toke_test_harness import classify_failure, extract_error_codes

BASE = Path(__file__).resolve().parent.parent
TAGS = BASE / "results" / "tagged-toke-zero-pass.json"
FAILED_DIR = BASE / "results" / "107-R5" / "failed"
CATEGORIES = BASE / "categories"


def load_reqs() -> dict:
    out = {}
    for req in CATEGORIES.glob("*/requirements.yaml"):
        try:
            specs = yaml.safe_load(req.read_text())
        except Exception:
            continue
        for s in specs or []:
            if "id" in s:
                out[s["id"]] = s
    return out


def detect_spec_issues(spec: dict) -> list:
    """Heuristics for spec-side problems."""
    issues = []
    desc = (spec.get("description") or "") + " " + (spec.get("output_format") or "")
    desc_l = desc.lower()
    # Network/LLM/etc
    if any(kw in desc_l for kw in ["http get", "http post", "httpbin", "websocket", "fetches", "live api"]):
        issues.append("requires-network-missed")
    if "llm" in desc_l or "natural language" in desc_l:
        issues.append("requires-llm-missed")
    # Placeholder in expected_output
    for tc in spec.get("test_cases", []):
        exp = (tc.get("expected_output", "") or "").strip()
        # Spec uses _hex, _placeholder-like patterns
        if exp and (
            exp.startswith("<") and exp.endswith(">")
            or exp.endswith("_hex") or exp.endswith("_secret_hex") or exp == "placeholder"
            or "<" in exp and ">" in exp and len(exp) < 80
        ):
            issues.append(f"placeholder-expected: {exp[:50]}")
            break
    return issues


def main():
    tags = json.loads(TAGS.read_text())
    fail_ids = set()
    # Identify fails from R5 state files
    for w in range(1, 6):
        sf = BASE / "results" / "107-R5" / f"state-w{w}.json"
        if sf.exists():
            s = json.loads(sf.read_text())
            for f in s.get("failed", []):
                fail_ids.add(f.get("id") if isinstance(f, dict) else f)
    print(f"Total fails to review: {len(fail_ids)}")

    reqs = load_reqs()

    results = []
    for pid in sorted(fail_ids):
        spec = reqs.get(pid, {})
        category = spec.get("_category", "?")
        # Try to find category from tags
        if not category or category == "?":
            for t in tags["tags"]:
                if t["id"] == pid:
                    category = t["category"]
                    break

        # Locate the failure artefact
        fail_dir = FAILED_DIR / category / pid
        attempt_file = fail_dir / "last-attempt.tk"
        err_file = fail_dir / "error.log"

        rec = {"id": pid, "category": category, "spec_issues": detect_spec_issues(spec)}

        if not attempt_file.exists():
            rec["fail_class"] = "no-artefact"
            rec["error_codes"] = []
            results.append(rec)
            continue

        opus_src = attempt_file.read_text(errors="replace")
        rec["src_len"] = len(opus_src)

        # Re-classify via harness
        c = classify_failure(opus_src, spec.get("test_cases", []))
        rec["fail_class"] = c.get("category", "?")
        rec["error_codes"] = c.get("error_codes", [])
        rec["error_excerpt"] = (c.get("error_excerpt") or "")[:200]
        rec["actual"] = (c.get("actual_excerpt") or "")[:120]
        rec["expected"] = (c.get("expected_excerpt") or "")[:120]
        results.append(rec)

    # Aggregate
    by_class = Counter(r["fail_class"] for r in results)
    print("\n=== Fail class distribution ===")
    for k, v in by_class.most_common():
        print(f"  {v:3d}  {k}")

    ec = Counter()
    for r in results:
        for c in r.get("error_codes", []):
            ec[c] += 1
    if ec:
        print("\n=== Top error codes ===")
        for c, n in ec.most_common(10):
            print(f"  {n:3d}  {c}")

    spec_issues = Counter()
    for r in results:
        for si in r.get("spec_issues", []):
            tag = si.split(":")[0]
            spec_issues[tag] += 1
    if spec_issues:
        print("\n=== Spec-side issues found (heuristic) ===")
        for s, n in spec_issues.most_common():
            print(f"  {n:3d}  {s}")
        print("\n  Programs with spec issues:")
        for r in results:
            if r["spec_issues"]:
                print(f"    {r['id']} [{r['category']}]: {r['spec_issues']}")

    print("\n=== Per-category fail breakdown ===")
    by_cat = defaultdict(Counter)
    for r in results:
        by_cat[r["category"]][r["fail_class"]] += 1
    for cat in sorted(by_cat):
        items = by_cat[cat]
        line = ", ".join(f"{c}={n}" for c, n in sorted(items.items(), key=lambda x: -x[1]))
        print(f"  {cat:<20} {dict(items)}")

    # Per-program one-liner
    print("\n=== Per-program detail ===")
    for r in sorted(results, key=lambda x: (x["fail_class"], x["id"])):
        line = f"  {r['id']:<10} [{r['category']:<20}] {r['fail_class']:<18}"
        if r["fail_class"] in ("compile_fail", "build_fail"):
            line += f" codes={r['error_codes'][:3]}"
        elif r["fail_class"] == "wrong_output":
            line += f" got={r['actual']!r} want={r['expected']!r}"
        elif r["fail_class"] == "empty_output":
            line += f" expected={r['expected']!r}"
        if r["spec_issues"]:
            line += f"  SPEC_ISSUES={r['spec_issues']}"
        print(line)

    # Save full
    out_file = BASE / "results" / "107-R5" / "fail-categorization.json"
    out_file.write_text(json.dumps(results, indent=2))
    print(f"\nFull detail: {out_file}")


if __name__ == "__main__":
    main()
