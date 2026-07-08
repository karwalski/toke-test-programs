#!/usr/bin/env python3
"""Compiler-guided v0.3 `=`-equality -> `==` migration for the COMPILE_FAIL set.

For each program the compiler flags E2002 "= is assignment; use ==" at the exact
BYTE offset of the offending `=`. We replace each flagged `=` with `==`
(descending offset order so earlier offsets stay valid), recompile, and repeat
until no E2002-assignment remains. Then re-run the manifest test_cases. The `=`
the compiler flags is provably an equality in expression position, so the rewrite
is safe. Writes fixes in place (git-tracked)."""
import json, os, subprocess, sys, tempfile

ROOT = os.path.expanduser("~/tk/toke-test-programs")
TOKE = os.path.expanduser("~/tk/toke/toke")

def norm(s): return "\n".join(l.rstrip() for l in s.strip().splitlines())

def eq_offsets(path):
    r = subprocess.run([TOKE, path, "--allow-all", "--check", "--diag-json"],
                       capture_output=True, text=True, timeout=60)
    offs = []
    for line in (r.stdout + r.stderr).splitlines():
        try: d = json.loads(line)
        except Exception: continue
        if d.get("error_code") == "E2002" and "assignment" in d.get("message", ""):
            offs.append(d["pos"]["offset"])
    return sorted(set(offs))

def fix_file(path):
    for _ in range(60):
        offs = eq_offsets(path)
        if not offs:
            return True
        b = bytearray(open(path, "rb").read())
        for off in sorted(offs, reverse=True):
            if 0 <= off < len(b) and b[off:off+1] == b"=":
                b[off:off+1] = b"=="   # single '=' -> '=='
        open(path, "wb").write(bytes(b))
    return False

def compiles_and_passes(path, tcs):
    with tempfile.TemporaryDirectory() as td:
        bpath = td + "/b"
        r = subprocess.run([TOKE, path, "--allow-all", "--out", bpath],
                           capture_output=True, text=True, timeout=60)
        if r.returncode != 0 or not os.path.exists(bpath):
            return "COMPILE_FAIL"
        for tc in tcs:
            try:
                rr = subprocess.run([bpath], input=tc.get("input","") or "",
                                    capture_output=True, text=True, timeout=10)
            except subprocess.TimeoutExpired:
                return "RUN_FAIL"
            if 132 <= rr.returncode <= 139:
                return "RUN_FAIL"
            if norm(rr.stdout) != norm(tc.get("expected_output","")):
                return "WRONG_OUTPUT"
        return "PASS"

# map id -> (category, test_cases)
meta = {}
import glob
for cf in glob.glob(ROOT + "/results/library/*.json"):
    if cf.endswith("index.json"): continue
    d = json.load(open(cf))
    for p in d["programs"]:
        meta[p["id"]] = (d["category"], p.get("test_cases") or [])

ids = sys.argv[1:] or json.load(open(ROOT+"/reports/library-1460-FINAL.json"))["compile_fail_ids"]
out = {"PASS":[], "WRONG_OUTPUT":[], "COMPILE_FAIL":[], "RUN_FAIL":[], "NO_META":[]}
for pid in ids:
    if pid not in meta:
        out["NO_META"].append(pid); continue
    cat, tcs = meta[pid]
    sol = f"{ROOT}/results/solutions/{cat}/{pid}/solution.tk"
    if not os.path.exists(sol):
        out["COMPILE_FAIL"].append(pid); continue
    fix_file(sol)
    st = compiles_and_passes(sol, tcs)
    out[st].append(pid)
    print(f"  {pid}: {st}", flush=True)

print("\n== fix summary ==")
for k, v in out.items():
    if v: print(f"  {k}: {len(v)}")
json.dump(out, open(ROOT+"/reports/fix-eq-result.json","w"), indent=1)
