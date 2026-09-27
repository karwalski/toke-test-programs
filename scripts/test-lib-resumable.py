#!/usr/bin/env python3
"""Resumable 1460-library test: appends each program's result to a JSONL (flush
per line) and skips IDs already recorded, so a kill preserves progress and
re-running continues where it left off. Aggregate with --report.

--retest ID [ID ...] re-runs just those programs and rewrites their existing
lines in place (136.72), so a repaired or regressed program's record is
refreshed without re-running all 1460. TOKE_BIN / TP_ROOT override the
compiler and the checkout."""
import json, glob, os, subprocess, sys, tempfile

ROOT = os.environ.get("TP_ROOT") or os.path.expanduser("~/tk/toke-test-programs")
TOKE = os.environ.get("TOKE_BIN") or os.path.expanduser("~/tk/toke/toke")

def capflags(sol):
    """126.3: build with the program's own tkc.toml grants (ADR-0010), never
    --allow-all, so a missing grant fails its test instead of being masked.
    No manifest -> an empty config, so a stray ./tkc.toml cannot grant."""
    m = os.path.join(os.path.dirname(sol), "tkc.toml")
    return ["--config=" + m] if os.path.exists(m) else ["--config=/dev/null"]

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

def test_one(cat, p):
    """Build and run one library program; return its JSONL record."""
    pid = p["id"]
    rec = {"id": pid, "cat": cat, "ratio": p.get("byte_ratio"),
           "toke_bytes": p.get("toke_bytes"), "python_bytes": p.get("python_bytes")}
    sol = f"{ROOT}/results/solutions/{cat}/{pid}/solution.tk"
    if not os.path.exists(sol):
        rec["status"] = "NO_SOLUTION"; return rec
    tcs = p.get("test_cases") or []
    if not tcs:
        rec["status"] = "NO_TESTS"; return rec
    with tempfile.TemporaryDirectory() as td:
        b = td + "/b"
        try:
            r = subprocess.run([TOKE, sol, *capflags(sol), "--out", b],
                               capture_output=True, text=True, timeout=60)
        except subprocess.TimeoutExpired:
            rec["status"] = "COMPILE_FAIL"; rec["code"] = "COMPILE_TIMEOUT"; return rec
        if r.returncode != 0 or not os.path.exists(b):
            rec["status"] = "COMPILE_FAIL"
            rec["code"] = next((l.split('"error_code":"')[1].split('"')[0]
                                for l in (r.stdout+r.stderr).splitlines() if '"error_code"' in l), "")
            return rec
        status = "PASS"
        for tc in tcs:
            try:
                rr = subprocess.run([b], input=tc.get("input","") or "",
                                    capture_output=True, text=True, timeout=10)
            except subprocess.TimeoutExpired:
                status = "RUN_FAIL"; break
            if rr.returncode < 0 or rr.returncode >= 128:   # signal/crash (negative on POSIX)
                status = "RUN_FAIL"; break
            if norm(rr.stdout) != norm(tc.get("expected_output","")):
                status = "WRONG_OUTPUT"; break
        rec["status"] = status
    return rec

def programs():
    cats = sorted(f for f in glob.glob(ROOT + "/results/library/*.json") if not f.endswith("index.json"))
    for cf in cats:
        d = json.load(open(cf))
        for p in d["programs"]:
            yield d["category"], p

if "--retest" in sys.argv:
    want = set(sys.argv[sys.argv.index("--retest")+1:])
    fresh = {p["id"]: test_one(cat, p) for cat, p in programs() if p["id"] in want}
    missing = want - set(fresh)
    if missing:
        sys.exit(f"not in the library: {sorted(missing)}")
    lines = open(JSONL).read().splitlines()
    seen = set()
    for i, line in enumerate(lines):
        if line.strip():
            rid = json.loads(line)["id"]
            if rid in fresh:
                lines[i] = json.dumps(fresh[rid]); seen.add(rid)
    lines += [json.dumps(fresh[r]) for r in sorted(set(fresh) - seen)]
    open(JSONL, "w").write("\n".join(lines) + "\n")
    for rid in sorted(fresh):
        print(rid, fresh[rid]["status"], fresh[rid].get("code", ""))
    sys.exit(0)

done = load_done()
out = open(JSONL, "a", buffering=1)  # line-buffered
n = 0
for cat, p in programs():
    if p["id"] in done:
        continue
    n += 1
    out.write(json.dumps(test_one(cat, p))+"\n")
    if n % 50 == 0:
        print(f"...{n} new this run", file=sys.stderr, flush=True)
out.close()
print(f"done this run: {n} new")
report()
