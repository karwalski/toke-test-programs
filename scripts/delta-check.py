#!/usr/bin/env python3
"""Compare current compiler behaviour against the pre-fix baseline (lib-results.jsonl,
captured before this session's compiler fixes). Reports REGRESSED (was PASS, now
fail) and RECOVERED (was fail, now PASS) across all 1460. Resumable: writes
reports/delta.jsonl per program, skips done."""
import json, glob, os, subprocess, sys, tempfile
ROOT=os.path.expanduser("~/tk/toke-test-programs"); TOKE=os.path.expanduser("~/tk/toke/toke")
OUT=ROOT+"/reports/delta.jsonl"
def norm(s): return "\n".join(l.rstrip() for l in s.strip().splitlines())
base={}
for l in open(ROOT+"/reports/lib-results.jsonl"):
    if l.strip():
        r=json.loads(l); base[r["id"]]=r["status"]
done=set()
if os.path.exists(OUT):
    for l in open(OUT):
        if l.strip(): done.add(json.loads(l)["id"])
meta={}
for cf in glob.glob(ROOT+"/results/library/*.json"):
    if cf.endswith("index.json"): continue
    d=json.load(open(cf))
    for p in d["programs"]: meta[p["id"]]=(d["category"],p)
if "--report" in sys.argv:
    cur={}
    for l in open(OUT):
        if l.strip(): r=json.loads(l); cur[r["id"]]=r["status"]
    regr=[i for i in cur if base.get(i)=="PASS" and cur[i]!="PASS"]
    reco=[i for i in cur if base.get(i)!="PASS" and cur[i]=="PASS"]
    print(f"checked {len(cur)}/1460 | REGRESSED (was PASS): {len(regr)} -> {sorted(regr)}")
    print(f"RECOVERED (was fail): {len(reco)} -> {sorted(reco)}")
    sys.exit(0)
out=open(OUT,"a",buffering=1)
n=0
for pid,(cat,p) in meta.items():
    if pid in done: continue
    n+=1
    sol=f"{ROOT}/results/solutions/{cat}/{pid}/solution.tk"
    st="PASS"
    if not os.path.exists(sol): st="NO_SOL"
    else:
        with tempfile.TemporaryDirectory() as td:
            b=td+"/b"
            try: r=subprocess.run([TOKE,sol,"--allow-all","--out",b],capture_output=True,text=True,timeout=60)
            except: r=None
            if r is None or r.returncode!=0 or not os.path.exists(b): st="COMPILE_FAIL"
            else:
                for tc in (p.get("test_cases") or []):
                    try: rr=subprocess.run([b],input=tc.get("input","") or "",capture_output=True,text=True,timeout=10)
                    except: st="RUN_FAIL"; break
                    if rr.returncode<0 or rr.returncode>=128: st="CRASH"; break
                    if norm(rr.stdout)!=norm(tc.get("expected_output","")): st="WRONG"; break
    out.write(json.dumps({"id":pid,"status":st})+"\n")
    if n%100==0: print(f"...{n} new",file=sys.stderr,flush=True)
print(f"done {n} new")
