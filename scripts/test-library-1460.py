#!/usr/bin/env python3
"""Test the 1460 dual-verified library programs against their manifest test cases.

For each program in results/library/<category>.json: compile the CURRENT
results/solutions/<category>/<id>/solution.tk (v0.4) and run every test_case
(stdin input -> compare stdout to expected_output). Also records byte_ratio so
we can target the 'toke larger than python' optimization set.
"""
import json, glob, os, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKE = os.path.expanduser("~/tk/toke/toke")
SOL = os.path.join(ROOT, "results", "solutions")

def norm(s): return "\n".join(l.rstrip() for l in s.strip().splitlines())

cats = sorted(f for f in glob.glob(os.path.join(ROOT, "results", "library", "*.json"))
              if not f.endswith("index.json"))
totals = dict(PASS=0, WRONG_OUTPUT=0, COMPILE_FAIL=0, RUN_FAIL=0, NO_SOLUTION=0, NO_TESTS=0)
fails = []            # (id, status, detail)
toke_bigger = []      # (id, byte_ratio, toke_bytes, python_bytes) where toke > python
n = 0
for cf in cats:
    d = json.load(open(cf))
    catkey = d["category"]
    for p in d["programs"]:
        n += 1
        pid = p["id"]
        br = p.get("byte_ratio")
        if br is not None and br < 1.0:
            toke_bigger.append((pid, br, p.get("toke_bytes"), p.get("python_bytes")))
        sol = os.path.join(SOL, catkey, pid, "solution.tk")
        if not os.path.exists(sol):
            totals["NO_SOLUTION"] += 1; fails.append((pid, "NO_SOLUTION", sol)); continue
        tcs = p.get("test_cases") or []
        if not tcs:
            totals["NO_TESTS"] += 1; continue
        with tempfile.TemporaryDirectory() as td:
            binp = os.path.join(td, "b")
            r = subprocess.run([TOKE, sol, "--allow-all", "--out", binp],
                               capture_output=True, text=True, timeout=60)
            if r.returncode != 0 or not os.path.exists(binp):
                totals["COMPILE_FAIL"] += 1
                code = ""
                for line in (r.stdout + r.stderr).splitlines():
                    if '"error_code"' in line:
                        code = line.split('"error_code":"')[1].split('"')[0]; break
                fails.append((pid, "COMPILE_FAIL", code)); continue
            ok = True; detail = ""
            for tc in tcs:
                inp = tc.get("input", "") or ""
                exp = tc.get("expected_output", "")
                try:
                    rr = subprocess.run([binp], input=inp, capture_output=True,
                                        text=True, timeout=10)
                except subprocess.TimeoutExpired:
                    ok = False; detail = "TIMEOUT"; totals["RUN_FAIL"] += 1; break
                if rr.returncode >= 132 and rr.returncode <= 139:
                    ok = False; detail = f"CRASH(sig {rr.returncode-128})"; totals["RUN_FAIL"] += 1; break
                if norm(rr.stdout) != norm(exp):
                    ok = False; detail = f"got={norm(rr.stdout)[:40]!r} want={norm(exp)[:40]!r}"
                    totals["WRONG_OUTPUT"] += 1; break
            if ok:
                totals["PASS"] += 1
            else:
                fails.append((pid, detail.split("(")[0] if "CRASH" in detail else
                              ("RUN_FAIL" if detail=="TIMEOUT" else "WRONG_OUTPUT"), detail))
        if n % 100 == 0:
            print(f"...{n} done (PASS={totals['PASS']})", file=sys.stderr)

print(f"\n===== LIBRARY 1460 TEST RESULTS ({n} programs) =====")
for k in ("PASS","WRONG_OUTPUT","COMPILE_FAIL","RUN_FAIL","NO_SOLUTION","NO_TESTS"):
    print(f"  {k}: {totals[k]}")
print(f"\nFailures ({len(fails)}):")
from collections import Counter
bycode = Counter()
for pid, st, det in fails:
    bycode[st] += 1
for st, c in bycode.most_common():
    print(f"  {st}: {c}")
print(f"\n'toke LARGER than python' (byte_ratio<1): {len(toke_bigger)} programs")
json.dump({"totals": totals, "fails": fails, "toke_bigger": sorted(toke_bigger, key=lambda x: x[1])},
          open(os.path.join(ROOT, "reports", "library-1460-test.json"), "w"), indent=1)
print("report -> reports/library-1460-test.json")
