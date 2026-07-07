#!/usr/bin/env python3
"""Resumable 1460-library test: appends each program's result to a JSONL (flush
per line) and skips IDs already recorded, so a kill preserves progress and
re-running continues where it left off. Aggregate with --report."""
import json, glob, os, subprocess, sys, tempfile

ROOT = os.path.expanduser("~/tk/toke-test-programs")
TOKE = os.path.expanduser("~/tk/toke/toke")
JSONL = os.path.join(ROOT, "reports", "lib-results.jsonl")

def norm(s): return "\n".join(l.rstrip() for l in s.strip().splitlines())

def load_done():
    done = {}
    if os.path.exists(JSONL):
        for line in open(JSONL):
            line = line.strip()
            if line:
                try:
                    r = json.loads(line); done[r["id"]] = r
                except Exception:
                    pass
    return done

def report():
    from collections import Counter
    done = load_done()
    tot = Counter(r["status"] for r in done.values())
    big = [r for r in done.values() if r.get("ratio") is not None and r["ratio"] < 1.0]
    print(f"===== LIBRARY 1460 TEST — {len(done)} recorded =====")
    for k in ("PASS", "WRONG_OUTPUT", "COMPILE_FAIL", "RUN_FAIL", "NO_SOLUTION", "NO_TESTS"):
        print(f"  {k}: {tot.get(k, 0)}")
    if done:
        print(f"  PASS rate: {tot.get('PASS',0)}/{len(done)} = {100*tot.get('PASS',0)/len(done):.1f}%")
    cc = Counter(r.get("code","") for r in done.values() if r["status"]=="COMPILE_FAIL" and r.get("code"))
    print("  COMPILE_FAIL by error code:", dict(cc.most_common(6)))
    print(f"  toke>python (ratio<1): {len(big)}")
    return

if "--report" in sys.argv:
    report(); sys.exit(0)

done = load_done()
cats = sorted(f for f in glob.glob(ROOT + "/results/library/*.json") if not f.endswith("index.json"))
out = open(JSONL, "a", buffering=1)  # line-buffered
n = 0
for cf in cats:
    d = json.load(open(cf)); cat = d["category"]
    for p in d["programs"]:
        pid = p["id"]
        if pid in done:
            continue
        n += 1
        rec = {"id": pid, "cat": cat, "ratio": p.get("byte_ratio"),
               "toke_bytes": p.get("toke_bytes"), "python_bytes": p.get("python_bytes")}
        sol = f"{ROOT}/results/solutions/{cat}/{pid}/solution.tk"
        if not os.path.exists(sol):
            rec["status"] = "NO_SOLUTION"; out.write(json.dumps(rec)+"\n"); continue
        tcs = p.get("test_cases") or []
        if not tcs:
            rec["status"] = "NO_TESTS"; out.write(json.dumps(rec)+"\n"); continue
        with tempfile.TemporaryDirectory() as td:
            b = td + "/b"
            try:
                r = subprocess.run([TOKE, sol, "--allow-all", "--out", b],
                                   capture_output=True, text=True, timeout=60)
            except subprocess.TimeoutExpired:
                rec["status"] = "COMPILE_FAIL"; rec["code"] = "COMPILE_TIMEOUT"
                out.write(json.dumps(rec)+"\n"); continue
            if r.returncode != 0 or not os.path.exists(b):
                rec["status"] = "COMPILE_FAIL"
                rec["code"] = next((l.split('"error_code":"')[1].split('"')[0]
                                    for l in (r.stdout+r.stderr).splitlines() if '"error_code"' in l), "")
                out.write(json.dumps(rec)+"\n"); continue
            status = "PASS"
            for tc in tcs:
                try:
                    rr = subprocess.run([b], input=tc.get("input","") or "",
                                        capture_output=True, text=True, timeout=10)
                except subprocess.TimeoutExpired:
                    status = "RUN_FAIL"; break
                if 132 <= rr.returncode <= 139:
                    status = "RUN_FAIL"; break
                if norm(rr.stdout) != norm(tc.get("expected_output","")):
                    status = "WRONG_OUTPUT"; break
            rec["status"] = status; out.write(json.dumps(rec)+"\n")
        if n % 50 == 0:
            print(f"...{n} new this run", file=sys.stderr, flush=True)
out.close()
print(f"done this run: {n} new")
report()
