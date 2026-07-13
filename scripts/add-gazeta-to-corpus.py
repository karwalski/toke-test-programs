#!/usr/bin/env python3
"""Add every PASSING gazeta-work/P###.tk to the corpus as the 'gazeta' category.
Builds results/solutions/gazeta/GAZ-###/solution.tk + results/library/gazeta.json
with test_cases derived from the program's impl/cases/*.in|.out."""
import os, glob, json, subprocess, tempfile, re
ROOT=os.path.expanduser("~/tk/toke-test-programs")
GAZ=os.path.expanduser("~/claude-gazeta-de-informatica/programs")
TOKE=os.path.expanduser("~/tk/toke/toke")
WORK=ROOT+"/gazeta-work"
def norm(s): return "\n".join(l.rstrip() for l in s.rstrip("\n").splitlines())
def title_from_slug(slug):
    parts=slug.split("-")[1:]
    return " ".join(w.capitalize() for w in parts)
progs=[]; added=0; skipped=[]
for tf in sorted(glob.glob(WORK+"/P*.tk")):
    pid=os.path.basename(tf)[:-3]                       # P002
    num=pid[1:]
    gid=f"GAZ-{num}"
    pdirs=glob.glob(f"{GAZ}/{pid}-*")
    if not pdirs: skipped.append((pid,"no-prog-dir")); continue
    pdir=pdirs[0]; slug=os.path.basename(pdir)
    src=open(tf).read()
    # verify it compiles + passes all cases
    cases=sorted(glob.glob(f"{pdir}/impl/cases/*.in"))
    tcs=[]
    with tempfile.TemporaryDirectory() as td:
        b=td+"/b"
        r=subprocess.run([TOKE,tf,"--allow-all","--out",b],capture_output=True,text=True,timeout=60)
        if r.returncode!=0 or not os.path.exists(b): skipped.append((pid,"compile")); continue
        ok=True
        for inf in cases:
            exp=open(inf[:-3]+".out").read(); inp=open(inf).read()
            try: rr=subprocess.run([b],input=inp,capture_output=True,text=True,timeout=10)
            except: ok=False; break
            if norm(rr.stdout)!=norm(exp): ok=False; break
            tcs.append({"input":inp,"expected_output":exp})
        if not ok: skipped.append((pid,"case-fail")); continue
    # write solution + manifest entry
    os.makedirs(f"{ROOT}/results/solutions/gazeta/{gid}",exist_ok=True)
    open(f"{ROOT}/results/solutions/gazeta/{gid}/solution.tk","w").write(src)
    pyf=f"{pdir}/impl/python/solution.py"
    pyb=os.path.getsize(pyf) if os.path.exists(pyf) else 0
    tb=len(src.encode())
    progs.append({"id":gid,"title":title_from_slug(slug),
        "description":f"Gazeta de Informatică program {pid} ({slug}).",
        "difficulty":2,"stdlib_modules":["std.io","std.str"],
        "input_format":"stdin (whitespace tokens)","output_format":"stdout",
        "source":src,"test_cases":tcs,
        "toke_bytes":tb,"python_bytes":pyb,
        "byte_ratio":round(pyb/tb,4) if tb else 0})
    added+=1
progs.sort(key=lambda p:p["id"])
man={"category":"gazeta","title":"Gazeta de Informatică (1991–92)","programs":progs}
json.dump(man, open(f"{ROOT}/results/library/gazeta.json","w"), indent=1)
print(f"added {added} programs to the gazeta category")
print(f"skipped {len(skipped)}: {skipped}")
