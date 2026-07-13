#!/usr/bin/env python3
"""Test a toke translation of a Gazeta program against its Python-derived cases.
Usage: test-gazeta.py <P###-slug> [toke_file]
Compiles the toke solution and runs every impl/cases/*.in, diffing stdout vs .out."""
import sys, os, glob, subprocess, tempfile
GAZ=os.path.expanduser("~/claude-gazeta-de-informatica/programs")
TOKE=os.path.expanduser("~/tk/toke/toke")
slug=sys.argv[1]
# resolve program dir (slug may be just P### or full)
cand=glob.glob(f"{GAZ}/{slug}*") if not os.path.isdir(f"{GAZ}/{slug}") else [f"{GAZ}/{slug}"]
if not cand: print(f"NO_PROGRAM {slug}"); sys.exit(2)
pdir=cand[0]; pid=os.path.basename(pdir).split("-")[0]
tokef=sys.argv[2] if len(sys.argv)>2 else os.path.expanduser(f"~/tk/toke-test-programs/gazeta-work/{pid}.tk")
if not os.path.exists(tokef): print(f"NO_TOKE {tokef}"); sys.exit(2)
cases=sorted(glob.glob(f"{pdir}/impl/cases/*.in"))
with tempfile.TemporaryDirectory() as td:
    b=td+"/b"
    r=subprocess.run([TOKE,tokef,"--allow-all","--out",b],capture_output=True,text=True,timeout=60)
    if r.returncode!=0 or not os.path.exists(b):
        code=next((l.split('"error_code":"')[1].split('"')[0] for l in (r.stdout+r.stderr).splitlines() if '"error_code"' in l),"")
        msg=next((l.split('"message":"')[1].split('"')[0] for l in (r.stdout+r.stderr).splitlines() if '"message"' in l),"")
        print(f"{pid}: COMPILE_FAIL {code} {msg}"); sys.exit(1)
    npass=0; fails=[]
    for inf in cases:
        base=inf[:-3]; exp=open(base+".out").read()
        inp=open(inf).read()
        try: rr=subprocess.run([b],input=inp,capture_output=True,text=True,timeout=10)
        except subprocess.TimeoutExpired: fails.append((os.path.basename(inf),"TIMEOUT")); continue
        got=rr.stdout
        if got.rstrip("\n")==exp.rstrip("\n"): npass+=1
        else: fails.append((os.path.basename(inf), f"got={got.rstrip()[:60]!r} want={exp.rstrip()[:60]!r}"))
    if fails:
        print(f"{pid}: FAIL {npass}/{len(cases)}")
        for f,d in fails[:4]: print(f"   {f}: {d}")
        sys.exit(1)
    print(f"{pid}: PASS {npass}/{len(cases)}"); sys.exit(0)
