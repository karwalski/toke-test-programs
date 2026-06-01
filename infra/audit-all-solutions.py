#!/usr/bin/env python3
"""audit-all-solutions.py — corpus-wide pass-quality audit.

Re-runs every solution.tk in results/solutions/ against ALL its test_cases
(strict equality, matches worker semantics). Classifies each program:

  - GENUINE        : real implementation (reads stdin, branches, computes,
                     multi-function or has loops)
  - TRIVIAL        : single println("constant"), no real logic
  - DUAL-BRANCH-SAME-OUTPUT : if/el both print same constant
  - PLACEHOLDER-PASS        : matches a spec with <hex>/<sig>/_hex placeholder
  - REGRESSED      : fails compile/build/test (was previously passing)

Output: results/solutions-audit.json with verdict per program.

Use case: catch trivial passes from prior runs (R3 AIA + R5) that aren't in
the R5 audit. Builds the authoritative "real" toke pass count.
"""

import json
import re
import sys
import subprocess
import tempfile
from collections import Counter
from pathlib import Path

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
        cat = req.parent.name
        try:
            specs = yaml.safe_load(req.read_text())
        except Exception:
            continue
        for s in specs or []:
            if "id" in s:
                s["_category"] = cat
                out[s["id"]] = s
    return out


def is_placeholder(s: str) -> bool:
    if not s:
        return False
    if re.match(r"^<[\w_/]+>$", s.strip()):
        return True
    if s.endswith("_hex") or s.endswith("_placeholder"):
        return True
    if "<hex>" in s or "<sig>" in s or "<base64>" in s:
        return True
    return False


def is_dual_branch_same_output(src: str) -> bool:
    """Detect `if(...){io.println("X")}el{io.println("X")}` patterns."""
    # find all println string literals
    matches = re.findall(r'io\.println\s*\(\s*"([^"]+)"\s*\)', src)
    if len(matches) < 2:
        return False
    # if many distinct messages, it's normal
    return len(set(matches)) == 1


def classify(pid: str, src: str, spec: dict) -> dict:
    tcs = spec.get("test_cases", [])
    has_loop = "lp(" in src
    has_branching = any(kw in src for kw in ["if(", "el{", "mt{"])
    has_helpers = src.count("f=") > 1  # more than just main
    reads_stdin = "io.readln" in src
    src_len = len(src)

    # Build + run all tests
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        staged = td / "solution.tk"
        staged.write_text(src)
        ok, _ = compile_check(staged)
        if not ok:
            return {"verdict": "REGRESSED-COMPILE", "src_len": src_len}
        bin_path = td / "bin"
        ok, _ = build(staged, bin_path)
        if not ok:
            return {"verdict": "REGRESSED-BUILD", "src_len": src_len}
        all_pass = True
        details = []
        for i, tc in enumerate(tcs):
            stdin = tc.get("input", "") or ""
            expected = (tc.get("expected_output", "") or "").strip()
            try:
                r = subprocess.run([str(bin_path)], input=stdin, capture_output=True,
                                   text=True, timeout=10, errors="replace")
                actual = (r.stdout or "").strip()
                strict_ok = r.returncode == 0 and actual == expected
            except subprocess.TimeoutExpired:
                strict_ok, actual = False, "TIMEOUT"
            if not strict_ok:
                all_pass = False
                details.append({"test": i + 1, "actual": actual[:120], "expected": expected[:120]})

        if not all_pass:
            return {"verdict": "REGRESSED-RUN", "src_len": src_len, "failed_tests": details}

    # Passes — now classify quality
    exp_vals = [(t.get("expected_output", "") or "").strip() for t in tcs]
    # Placeholder spec
    if any(is_placeholder(v) for v in exp_vals):
        return {"verdict": "PLACEHOLDER-PASS", "src_len": src_len, "expected": exp_vals[:1]}
    # Dual-branch trivially printing the same thing
    if is_dual_branch_same_output(src) and len(set(exp_vals)) == 1:
        return {"verdict": "DUAL-BRANCH-SAME-OUTPUT", "src_len": src_len}
    # Trivial: tiny + no loop + no branching + ONLY main
    if src_len < 200 and not has_loop and not has_branching and not has_helpers:
        return {"verdict": "TRIVIAL", "src_len": src_len, "reason": "tiny no-logic single-main"}
    # Tiny but with branching/main only: SUSPECT
    if src_len < 200 and not has_loop and not has_helpers:
        return {"verdict": "SUSPECT", "src_len": src_len, "reason": "tiny one-branch"}
    return {"verdict": "GENUINE", "src_len": src_len,
            "structural": {"loop": has_loop, "if": has_branching, "helpers": has_helpers}}


def main():
    reqs = load_reqs()
    sols = sorted(SOLUTIONS.glob("*/*/solution.tk"))
    print(f"Auditing {len(sols)} solutions across {len({s.parent.parent.name for s in sols})} categories")

    results = []
    counters = Counter()
    for sol_path in sols:
        pid = sol_path.parent.name
        cat = sol_path.parent.parent.name
        spec = reqs.get(pid)
        if not spec:
            counters["no-spec"] += 1
            results.append({"id": pid, "category": cat, "verdict": "NO-SPEC"})
            continue
        src = sol_path.read_text(errors="replace")
        verdict_info = classify(pid, src, spec)
        verdict = verdict_info["verdict"]
        counters[verdict] += 1
        results.append({"id": pid, "category": cat, **verdict_info})

    print("\n=== Verdict distribution ===")
    for k, v in counters.most_common():
        print(f"  {v:4d}  {k}")

    print("\n=== Per-category × per-verdict ===")
    by_cat: dict[str, Counter] = {}
    for r in results:
        by_cat.setdefault(r["category"], Counter())[r["verdict"]] += 1
    for cat in sorted(by_cat):
        items = ", ".join(f"{k}={v}" for k, v in by_cat[cat].most_common())
        print(f"  {cat:<22} {items}")

    print("\n=== Programs to investigate (non-GENUINE) ===")
    for r in sorted(results, key=lambda x: (x["verdict"], x["id"])):
        if r["verdict"] in ("GENUINE",):
            continue
        extra = ""
        if r.get("expected"):
            extra = f" expected={r['expected']}"
        elif r.get("reason"):
            extra = f" {r['reason']}"
        elif r.get("failed_tests"):
            t = r["failed_tests"][0]
            extra = f" failed_t{t['test']}: got={t['actual'][:60]!r} want={t['expected'][:60]!r}"
        print(f"  {r['id']:<10} [{r['category']:<22}] {r['verdict']:<25}{extra}")

    out_file = BASE / "results" / "solutions-audit.json"
    out_file.write_text(json.dumps({"counters": dict(counters), "results": results}, indent=2))
    print(f"\nFull: {out_file}")


if __name__ == "__main__":
    main()
