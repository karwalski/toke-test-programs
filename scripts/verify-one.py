#!/usr/bin/env python3
"""Verify a single library program: compile its solution.tk and run every
manifest test_case (exact stdout match). Prints PASS/<FAIL reason> + byte count.
Usage: verify-one.py <PROGRAM_ID>   (e.g. verify-one.py DAT-072)
Exit 0 = PASS (safe to keep the rewrite), non-zero = FAIL (revert)."""
import json, glob, os, subprocess, sys, tempfile

ROOT = os.path.expanduser("~/tk/toke-test-programs")
TOKE = os.path.expanduser("~/tk/toke/toke")

def norm(s): return "\n".join(l.rstrip() for l in s.strip().splitlines())

pid = sys.argv[1]
meta = None
for cf in glob.glob(ROOT + "/results/library/*.json"):
    if cf.endswith("index.json"): continue
    d = json.load(open(cf))
    for p in d["programs"]:
        if p["id"] == pid:
            meta = (d["category"], p); break
    if meta: break
if not meta:
    print(f"{pid}: NO_META"); sys.exit(2)
cat, p = meta
sol = f"{ROOT}/results/solutions/{cat}/{pid}/solution.tk"
nbytes = os.path.getsize(sol)
with tempfile.TemporaryDirectory() as td:
    b = td + "/b"
    r = subprocess.run([TOKE, sol, "--allow-all", "--out", b], capture_output=True, text=True, timeout=60)
    if r.returncode != 0 or not os.path.exists(b):
        code = next((l.split('"error_code":"')[1].split('"')[0]
                     for l in (r.stdout+r.stderr).splitlines() if '"error_code"' in l), "")
        print(f"{pid}: COMPILE_FAIL {code}"); sys.exit(1)
    for i, tc in enumerate(p.get("test_cases") or []):
        fx = tc.get("fixtures") or {}
        for d in fx.get("dirs", []):
            os.makedirs(d, exist_ok=True)
        for fpath, content in (fx.get("files") or {}).items():
            os.makedirs(os.path.dirname(fpath), exist_ok=True)
            open(fpath,"wb").write(content.encode("latin-1"))
        try:
            rr = subprocess.run([b], input=tc.get("input","") or "", capture_output=True, text=True, timeout=10)
        except subprocess.TimeoutExpired:
            print(f"{pid}: TIMEOUT (test {i})"); sys.exit(1)
        if rr.returncode < 0 or rr.returncode >= 128:
            print(f"{pid}: CRASH sig {abs(rr.returncode)} (test {i})"); sys.exit(1)
        if norm(rr.stdout) != norm(tc.get("expected_output","")):
            print(f"{pid}: WRONG_OUTPUT (test {i}) got={norm(rr.stdout)[:50]!r} want={norm(tc.get('expected_output',''))[:50]!r}")
            sys.exit(1)
print(f"{pid}: PASS  bytes={nbytes}")
sys.exit(0)
