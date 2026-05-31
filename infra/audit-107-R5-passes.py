#!/usr/bin/env python3
"""audit-107-R5-passes.py — verify every 'pass' in 107.R5 is genuine.

For each completed program:
  1. Re-run solution.tk against ALL test_cases with current local tkc
     (independent of worker — uses toke_test_harness)
  2. Flag trivial echo-the-placeholder solutions (model just prints a literal
     that happens to match the spec's literal expected_output)
  3. Flag specs with placeholder patterns in expected_output (`<hex>`, `_hex`,
     `<sig>`, etc.) that make "passing" cheap
  4. Detect when all test cases share the same expected_output (single-output
     hard-code is enough to pass)

Output: results/107-R5/pass-audit.json with verdict per program.
"""

import json
import re
import sys
import subprocess
import tempfile
from pathlib import Path
from collections import Counter

import yaml

sys.path.insert(0, str(Path(__file__).parent))
from toke_test_harness import compile_check, build, run_test

BASE = Path(__file__).resolve().parent.parent
CATEGORIES = BASE / "categories"
SOLUTIONS = BASE / "results" / "solutions"
TKC = "/Users/matthew.watt/tk/toke/tkc"


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


PLACEHOLDER_PATTERNS = [
    (r"^<[\w_/]+>$", "angle-bracket placeholder"),  # <hex>, <sig>
    (r"_hex$", "trailing _hex placeholder"),
    (r"_placeholder", "explicit _placeholder"),
    (r"<hex>", "<hex> embedded"),
    (r"<sig>", "<sig> embedded"),
    (r"<base64>", "<base64> embedded"),
    (r"<.*?>", "any angle-bracket token (loose)"),
]


def detect_spec_placeholders(test_cases: list) -> list:
    """Flag any test case whose expected_output looks like a placeholder."""
    issues = []
    for i, tc in enumerate(test_cases):
        exp = (tc.get("expected_output", "") or "").strip()
        for pat, desc in PLACEHOLDER_PATTERNS:
            if re.search(pat, exp):
                # Skip cases where the angle bracket is clearly real markup (e.g., HTML)
                if pat == r"<.*?>" and any(tag in exp.lower() for tag in ["<p>", "<ul>", "<li>", "<nav>", "<a ", "<div>", "<span>", "<h1>", "<table>"]):
                    # HTML — real markup, not placeholder
                    continue
                issues.append(f"test_{i+1} matches '{desc}': {exp[:80]}")
                break
    return issues


def is_trivial_echo(src: str, test_cases: list) -> tuple[bool, str]:
    """Detect if the program just hardcodes println(<literal>) matching expected.
    Returns (is_trivial, reason)."""
    if not test_cases:
        return False, ""
    expected_values = {(tc.get("expected_output", "") or "").strip() for tc in test_cases}
    # If all tests share one expected value AND that value appears as a literal
    # in the source, this is likely just an echo
    if len(expected_values) == 1:
        exp = next(iter(expected_values))
        if exp and exp in src:
            # Check if main() body is suspiciously simple — short or just an io.println
            return True, f"single expected '{exp[:60]}' appears as literal in source ({len(src)}b)"
    # Multi-output: check if all expected values appear as literals in source
    if expected_values and all(v and v in src for v in expected_values):
        return True, f"all expected outputs ({len(expected_values)} unique) appear as literals in source"
    return False, ""


def main():
    completed = []
    for w in range(1, 6):
        sf = BASE / "results" / "107-R5" / f"state-w{w}.json"
        if sf.exists():
            s = json.loads(sf.read_text())
            completed.extend(s.get("completed", []))
    completed = sorted(set(completed))
    print(f"Auditing {len(completed)} passes")

    reqs = load_reqs()
    results = []
    counters = Counter()

    for pid in completed:
        spec = reqs.get(pid, {})
        if not spec:
            results.append({"id": pid, "verdict": "no-spec", "notes": "spec not found"})
            counters["no-spec"] += 1
            continue

        cat = spec.get("_category", "?")
        # category from spec — but our reqs use file-based loading. Find by id-prefix match
        for req_file in CATEGORIES.glob("*/requirements.yaml"):
            try:
                if any(s.get("id") == pid for s in yaml.safe_load(req_file.read_text())):
                    cat = req_file.parent.name
                    break
            except Exception:
                pass

        sol_path = SOLUTIONS / cat / pid / "solution.tk"
        if not sol_path.exists():
            results.append({"id": pid, "category": cat, "verdict": "no-source", "notes": "solution.tk missing"})
            counters["no-source"] += 1
            continue
        src = sol_path.read_text(errors="replace")
        tcs = spec.get("test_cases", [])

        # Build the binary
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            staged = td / "solution.tk"
            staged.write_text(src)
            ok, out = compile_check(staged)
            if not ok:
                results.append({"id": pid, "category": cat, "verdict": "REGRESSED-COMPILE",
                                "notes": f"src now fails compile: {out[:200]}"})
                counters["regressed-compile"] += 1
                continue
            bin_path = td / "bin"
            ok, out = build(staged, bin_path)
            if not ok:
                results.append({"id": pid, "category": cat, "verdict": "REGRESSED-BUILD",
                                "notes": f"src now fails build: {out[:200]}"})
                counters["regressed-build"] += 1
                continue

            # Run ALL test cases with strict equality (matches worker semantics)
            all_strict_pass = True
            tolerant_only = False
            test_details = []
            for i, tc in enumerate(tcs):
                stdin = tc.get("input", "") or ""
                expected = (tc.get("expected_output", "") or "").strip()
                try:
                    r = subprocess.run([str(bin_path)], input=stdin, capture_output=True,
                                       text=True, timeout=10, errors="replace")
                    actual = (r.stdout or "").strip()
                    strict_ok = (r.returncode == 0) and (actual == expected)
                    if not strict_ok:
                        all_strict_pass = False
                        # Try tolerant via harness
                        tol_ok, _, _ = run_test(bin_path, stdin, expected)
                        if tol_ok:
                            tolerant_only = True
                        test_details.append({
                            "test": i + 1, "strict": strict_ok, "tolerant": tol_ok,
                            "actual": actual[:120], "expected": expected[:120],
                            "rc": r.returncode,
                        })
                except subprocess.TimeoutExpired:
                    all_strict_pass = False
                    test_details.append({"test": i + 1, "strict": False, "actual": "TIMEOUT"})

        # Spec issue detection
        spec_issues = detect_spec_placeholders(tcs)
        trivial, trivial_reason = is_trivial_echo(src, tcs)

        if not all_strict_pass:
            if tolerant_only:
                verdict = "TOLERANT-ONLY"
                counters["tolerant-only"] += 1
            else:
                verdict = "REGRESSED-RUN"
                counters["regressed-run"] += 1
        elif spec_issues and trivial:
            verdict = "TRIVIAL-VIA-PLACEHOLDER"
            counters["trivial-via-placeholder"] += 1
        elif trivial:
            verdict = "TRIVIAL-HARDCODE"
            counters["trivial-hardcode"] += 1
        elif spec_issues:
            verdict = "GENUINE-BUT-SPEC-WEAK"
            counters["genuine-but-spec-weak"] += 1
        else:
            verdict = "GENUINE"
            counters["genuine"] += 1

        results.append({
            "id": pid, "category": cat, "verdict": verdict,
            "src_bytes": len(src),
            "n_test_cases": len(tcs),
            "spec_issues": spec_issues,
            "trivial_reason": trivial_reason,
            "test_details": test_details if not all_strict_pass else [],
        })

    print("\n=== Verdict distribution ===")
    for k, v in counters.most_common():
        print(f"  {v:3d}  {k}")

    print("\n=== Per-verdict programs ===")
    for verdict in ["GENUINE", "GENUINE-BUT-SPEC-WEAK", "TOLERANT-ONLY",
                    "TRIVIAL-VIA-PLACEHOLDER", "TRIVIAL-HARDCODE",
                    "REGRESSED-COMPILE", "REGRESSED-BUILD", "REGRESSED-RUN"]:
        matching = [r for r in results if r["verdict"] == verdict]
        if not matching:
            continue
        print(f"\n  --- {verdict} ({len(matching)}) ---")
        for r in matching:
            line = f"    {r['id']:<10} [{r.get('category','?'):<20}]"
            if r.get("spec_issues"):
                line += f" SPEC={r['spec_issues'][0][:60]}"
            elif r.get("trivial_reason"):
                line += f" TRIVIAL={r['trivial_reason'][:60]}"
            elif r.get("test_details"):
                td = r["test_details"][0]
                line += f" got={td.get('actual', '')[:50]!r} want={td.get('expected', '')[:50]!r}"
            print(line)

    # Save full report
    out_file = BASE / "results" / "107-R5" / "pass-audit.json"
    out_file.write_text(json.dumps({"counters": dict(counters), "results": results}, indent=2))
    print(f"\nFull: {out_file}")


if __name__ == "__main__":
    main()
