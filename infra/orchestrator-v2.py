#!/usr/bin/env python3
"""orchestrator-v2.py — Manifest-driven dispatch of generation/repair work to workers.

Story 108.5.

Replaces the old hash-partition + incremental-skip approach. Local orchestrator
classifies every program from audit-report.json, decides per-program mode +
budget, splits across the available worker fleet, and writes per-worker manifest
JSON. deploy-worker.sh (108.4) ships the manifest. The worker processes ONLY
the list in its manifest, in order — no per-worker skipping logic.

Manifest schema (per worker):
    {
      "tkc_version": "0.3.9",
      "worker_id": 1,
      "generated_at": "2026-05-29T20:43:00Z",
      "mode": "baseline" | "repair" | "targeted" | "mixed",
      "programs": [
        {
          "id": "AIA-001",
          "category": "ai-agents",
          "mode": "baseline" | "repair",
          "max_iterations": 5,
          "model": "toke-api" | "sonnet" | "opus",
          "current_status": "NO_SOURCE",
          "hint": "..."        # from repair-hints.json
        }
      ]
    }

Usage:
    orchestrator-v2.py classify             # show stats + bucket counts
    orchestrator-v2.py plan --mode baseline # write manifests/ for empty progs
    orchestrator-v2.py plan --mode repair   # write manifests/ for failing progs
    orchestrator-v2.py plan --mode mixed --workers 1,2,3,4,5
    orchestrator-v2.py deploy --workers 1,2,3,4,5
    orchestrator-v2.py status               # remote heartbeat per worker
"""

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INFRA = Path(__file__).resolve().parent
AUDIT = ROOT / "results" / "audit-report.json"
HINTS = ROOT / "results" / "repair-hints.json"
WORKERS_FILE = INFRA / "workers.json"
MANIFEST_DIR = INFRA / "manifests"

DEPLOY_SCRIPT = INFRA / "deploy-worker.sh"

# Worker IPs are managed via workers.json:
#   { "1": "3.25.144.196", "2": "16.176.96.93", ... }
# IPs change on each Lightsail restart — refresh before runs.


def load_workers() -> dict[int, str]:
    if not WORKERS_FILE.exists():
        sys.exit(f"ERROR: {WORKERS_FILE} missing. Create with:\n"
                 f'  {{"1":"<ip1>","2":"<ip2>", ...}}')
    return {int(k): v for k, v in json.loads(WORKERS_FILE.read_text()).items()}


def load_audit() -> dict:
    if not AUDIT.exists():
        sys.exit(f"ERROR: {AUDIT} missing. Run local-audit.py first.")
    return json.loads(AUDIT.read_text())


def load_hints() -> dict:
    return json.loads(HINTS.read_text()) if HINTS.exists() else {}


# ── Held programs (Python ref broken/unverified — skip until fixed) ─────
HELD = ROOT / "results" / "held-programs.json"


def load_held_ids() -> set[str]:
    """Return set of program IDs that are on hold pending Python-ref repair.
    See results/held-programs.json for per-program reasoning. Orchestrator
    skips these in classify, plan, and deploy — no point spending Anthropic
    credit on toke generation when the Python reference itself is wrong."""
    if not HELD.exists():
        return set()
    try:
        data = json.loads(HELD.read_text())
        return {p["id"] for p in data.get("programs", [])}
    except (json.JSONDecodeError, OSError, KeyError):
        return set()


REFUSAL_PHRASES = (
    "i'm sorry", "i am sorry", "i cannot", "i can't",
    "i am not able", "i'm not able", "as an ai", "i do not assist",
)


def classify_program(prog: dict, hints: dict) -> str:
    """Map a program audit entry → canonical bucket.

    Buckets:
      runs_correct  — PASS
      runs_wrong    — WRONG_OUTPUT (or RUN_FAIL/SEGFAULT/TIMEOUT)
      build_fail    — BUILD_FAIL
      compile_fail  — COMPILE_FAIL with real source
      no_code       — refusal / truncated stub / very short
    """
    pid = prog["id"]
    status = prog.get("status", "")
    sb = prog.get("source_bytes", 0)

    # No-code signal: hint flagged truncated OR refusal text OR too short
    hint_entry = hints.get(pid, {})
    hint_msgs = " ".join(hint_entry.get("hints", [])) if hint_entry else ""
    if "CODE IS TRUNCATED" in hint_msgs:
        return "no_code"  # truncated stub from pre-v9 lambda
    if sb < 50:
        return "no_code"
    # Refusal: peek at the source
    cat = prog.get("category", "")
    src_path = ROOT / "results" / "solutions" / cat / pid / "solution.tk"
    if src_path.exists():
        try:
            preview = src_path.read_text(errors="replace")[:200].lower()
            if any(p in preview for p in REFUSAL_PHRASES):
                return "no_code"
        except OSError:
            pass

    if status == "PASS":
        return "runs_correct"
    if status in ("WRONG_OUTPUT", "RUN_FAIL", "SEGFAULT", "TIMEOUT"):
        return "runs_wrong"
    if status == "BUILD_FAIL":
        return "build_fail"
    if status == "COMPILE_FAIL":
        return "compile_fail"
    return "unknown"


def all_classifications(audit: dict, hints: dict) -> dict[str, str]:
    """Classify every program. Held programs (Python ref broken/unverified)
    are routed to the `held` bucket and excluded from any active mode."""
    held = load_held_ids()
    out: dict[str, str] = {}
    for p in audit["programs"]:
        if p["id"] in held:
            out[p["id"]] = "held"
        else:
            out[p["id"]] = classify_program(p, hints)
    return out


def cmd_classify(args):
    audit = load_audit()
    hints = load_hints()
    buckets = all_classifications(audit, hints)
    from collections import Counter
    counts = Counter(buckets.values())
    print(json.dumps({
        "total": len(buckets),
        "by_bucket": dict(counts.most_common()),
    }, indent=2))


def select_for_mode(buckets: dict[str, str], mode: str) -> list[str]:
    # `held` is always excluded — Python ref broken, fix that first.
    if mode == "baseline":
        return sorted([k for k, v in buckets.items() if v == "no_code"])
    if mode == "repair":
        return sorted([k for k, v in buckets.items()
                       if v in ("compile_fail", "build_fail", "runs_wrong")])
    if mode == "targeted":
        # build_fail + runs_wrong only (closest to working)
        return sorted([k for k, v in buckets.items()
                       if v in ("build_fail", "runs_wrong")])
    if mode == "mixed":
        # everything that isn't already passing AND not held
        return sorted([k for k, v in buckets.items()
                       if v not in ("runs_correct", "held")])
    sys.exit(f"unknown mode: {mode}")


def read_existing_source(category: str, pid: str) -> str:
    """Return the on-disk solution.tk content for a program, or empty string."""
    path = ROOT / "results" / "solutions" / category / pid / "solution.tk"
    if path.exists():
        try:
            return path.read_text(errors="replace")
        except OSError:
            return ""
    return ""


def cmd_plan(args):
    audit = load_audit()
    hints = load_hints()
    cat_map = {p["id"]: p["category"] for p in audit["programs"]}
    status_map = {p["id"]: p.get("status", "") for p in audit["programs"]}

    buckets = all_classifications(audit, hints)
    selected = select_for_mode(buckets, args.mode)
    if not selected:
        sys.exit("plan: no programs match this mode — nothing to do")

    worker_ids = [int(w) for w in args.workers.split(",")]
    n = len(worker_ids)
    # Round-robin assignment for even load
    assignments: dict[int, list[str]] = {wid: [] for wid in worker_ids}
    for i, pid in enumerate(selected):
        assignments[worker_ids[i % n]].append(pid)

    # Decide per-program mode + model + iteration budget by bucket
    max_sonnet_global = int(args.max_sonnet)
    max_opus_global = int(args.max_opus)

    def to_entry(pid: str) -> dict:
        b = buckets[pid]
        category = cat_map.get(pid, "")
        entry = {
            "id": pid,
            "category": category,
            "current_status": status_map.get(pid, ""),
            "bucket": b,
            "hint": " ".join(hints.get(pid, {}).get("hints", []))[:400],
            # Embed existing source so the worker is self-contained.
            "source": read_existing_source(category, pid),
        }
        # Per-program iteration budget (manifest-level defaults can be overridden later)
        entry["max_sonnet"] = max_sonnet_global
        entry["max_opus"] = max_opus_global
        if b == "no_code":
            entry.update(mode="baseline", model="toke-api")
        else:
            entry.update(mode="repair", model="sonnet")
        return entry

    MANIFEST_DIR.mkdir(exist_ok=True)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    written = []
    for wid, pids in assignments.items():
        manifest = {
            "tkc_version": "0.3.9",
            "worker_id": wid,
            "generated_at": now,
            "mode": args.mode,
            "programs": [to_entry(pid) for pid in pids],
        }
        path = MANIFEST_DIR / f"w{wid}.json"
        path.write_text(json.dumps(manifest, indent=2))
        written.append((wid, len(pids), path))

    print(f"plan: mode={args.mode}, total={len(selected)}, workers={n}")
    for wid, count, path in written:
        print(f"  w{wid}: {count:4d} programs → {path}")


def cmd_deploy(args):
    workers = load_workers()
    worker_ids = [int(w) for w in args.workers.split(",")]

    if not DEPLOY_SCRIPT.exists():
        sys.exit(f"ERROR: {DEPLOY_SCRIPT} missing")

    procs = []
    for wid in worker_ids:
        if wid not in workers:
            print(f"  WARN: w{wid} not in workers.json — skipping")
            continue
        ip = workers[wid]
        manifest = MANIFEST_DIR / f"w{wid}.json"
        if not manifest.exists():
            print(f"  WARN: {manifest} missing — run `plan` first")
            continue
        env_file = INFRA / f".env.w{wid}"
        cmd = [str(DEPLOY_SCRIPT), "-i", ip, "-w", str(wid),
               "-m", str(manifest)]
        if env_file.exists():
            cmd += ["-e", str(env_file)]
        print(f"  ==> w{wid} ({ip}) — deploying with {manifest.name}")
        procs.append((wid, subprocess.Popen(cmd)))

    rc = 0
    for wid, p in procs:
        if p.wait() != 0:
            print(f"  w{wid} deploy FAILED (rc={p.returncode})")
            rc = 1
    sys.exit(rc)


def cmd_collect(args):
    """Pull worker artefacts back to local `infra/collected/wN/`.

    Idempotent rsync. Safe to run mid-run for progressive results.
    """
    workers = load_workers()
    worker_ids = [int(w) for w in args.workers.split(",")]
    key = Path.home() / ".ssh" / "toke-workers-rsa"
    base = INFRA / "collected"
    base.mkdir(exist_ok=True)

    for wid in worker_ids:
        ip = workers.get(wid)
        if not ip:
            print(f"  w{wid}: no IP — skipping")
            continue
        dest = base / f"w{wid}"
        dest.mkdir(exist_ok=True)
        # rsync --rsync-path with sudo so we can read root-owned paths
        rsync_cmd = [
            "rsync", "-az",
            "--rsync-path=sudo rsync",
            "-e", f"ssh -i {key} -o BatchMode=yes -o StrictHostKeyChecking=accept-new",
            f"ubuntu@{ip}:/opt/toke-worker/solutions/",
            str(dest / "solutions") + "/",
        ]
        # Pull state, budget, logs, per-iteration attempts
        single_files = [
            ("state.json",  dest / "state.json"),
            ("budget.json", dest / "budget.json"),
            ("repair-hints.json", dest / "repair-hints.json"),
        ]
        print(f"  w{wid} ({ip}): pulling solutions/")
        subprocess.run(rsync_cmd, check=False)
        for name, local_path in single_files:
            subprocess.run([
                "scp", "-i", str(key), "-o", "BatchMode=yes",
                f"ubuntu@{ip}:/opt/toke-worker/{name}",
                str(local_path),
            ], check=False, capture_output=True)
        # Logs and attempts subtrees
        for sub in ("logs", "attempts"):
            subprocess.run([
                "rsync", "-az",
                "--rsync-path=sudo rsync",
                "-e", f"ssh -i {key} -o BatchMode=yes",
                f"ubuntu@{ip}:/opt/toke-worker/{sub}/",
                str(dest / sub) + "/",
            ], check=False)
        # Print compact summary
        budget_path = dest / "budget.json"
        spent = "?"
        if budget_path.exists():
            try:
                spent = f"${json.loads(budget_path.read_text())['usd_spent']:.4f}"
            except (json.JSONDecodeError, OSError, KeyError):
                pass
        print(f"  w{wid}: collected → {dest} (spend={spent})")


def cmd_status(args):
    """Lightweight heartbeat — does each worker have a manifest + tkc?"""
    workers = load_workers()
    worker_ids = [int(w) for w in (args.workers or
                                   ",".join(map(str, workers.keys()))).split(",")]
    key = Path.home() / ".ssh" / "toke-workers-rsa"
    for wid in worker_ids:
        ip = workers.get(wid)
        if not ip:
            print(f"  w{wid}: no IP")
            continue
        # Avoid pgrep matching its own argv: use `pgrep -f [w]orker-generate`
        cmd = ["ssh", "-i", str(key), "-o", "BatchMode=yes",
               "-o", "ConnectTimeout=8", f"ubuntu@{ip}",
               "echo tkc=$(tkc --version 2>&1 | head -1) "
               "manifest=$(ls /opt/toke-worker/manifests/ 2>/dev/null | head -1 || echo none) "
               "procs=$(pgrep -f '[w]orker-generate' | wc -l)"]
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        print(f"  w{wid} ({ip}): {out.stdout.strip() or 'unreachable'}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("classify", help="show bucket counts")

    p_plan = sub.add_parser("plan", help="write manifests")
    p_plan.add_argument("--mode", required=True,
                        choices=["baseline", "repair", "targeted", "mixed"])
    p_plan.add_argument("--workers", default="1,2,3,4,5")
    p_plan.add_argument("--max-sonnet", default="5",
                        help="Sonnet repair iterations per program (default 5)")
    p_plan.add_argument("--max-opus", default="0",
                        help="Opus repair iterations per program (default 0)")

    p_dep = sub.add_parser("deploy", help="ship manifests to workers")
    p_dep.add_argument("--workers", default="1,2,3,4,5")

    p_co = sub.add_parser("collect", help="rsync results back to infra/collected/")
    p_co.add_argument("--workers", default="1,2,3,4,5")

    p_st = sub.add_parser("status", help="worker heartbeat")
    p_st.add_argument("--workers", default="")

    args = parser.parse_args()
    {
        "classify": cmd_classify,
        "plan": cmd_plan,
        "deploy": cmd_deploy,
        "collect": cmd_collect,
        "status": cmd_status,
    }[args.cmd](args)


if __name__ == "__main__":
    main()
