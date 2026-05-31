#!/usr/bin/env python3
"""dry-run-workers.py — local pre-flight validation for a manifest set.

Spawns N worker subprocesses locally with DRY_RUN=1 + WORKER_ID + MANIFEST_PATH
+ WORKER_DIR set, runs them in parallel, collects state-dryrun.json from each,
reports per-worker outcome counts, asserts no crashes.

Catches:
  - prompt-format crashes (would IndexError on launch)
  - missing env vars (WORKER_ID unset → wrong manifest path)
  - manifest-shape issues (bad json, missing fields)
  - tkc binary issues (not in PATH, broken build)
  - subprocess unicode crashes
  - file-perm issues

Story 107.R4.1.

Usage:
    python3 infra/dry-run-workers.py [manifest_dir] [--workers N]

Defaults:
    manifest_dir: infra/manifests-py-repair/
    workers: 5
    looks for w{1..N}.json (or w{1..N}-full.json fallback) per worker
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DEFAULT_MANIFEST_DIR = BASE / "infra" / "manifests-py-repair"
WORKER_SCRIPT = BASE / "infra" / "worker-generate.py"
TKC = os.environ.get("TKC", "/Users/matthew.watt/tk/toke/tkc")


def find_manifest(manifest_dir: Path, wid: int) -> Path | None:
    """Look for w{wid}.json, w{wid}-full.json, w{wid}-toke-sample-50.json etc."""
    for stem in [f"w{wid}", f"w{wid}-full", f"w{wid}-toke-sample-50", f"w{wid}-retry", f"w{wid}-untouched"]:
        p = manifest_dir / f"{stem}.json"
        if p.exists():
            return p
    return None


def run_one_worker(wid: int, manifest: Path, sandbox_root: Path) -> dict:
    """Spawn worker-generate.py subprocess with DRY_RUN=1 + a temp WORKER_DIR.

    Sets up a self-contained sandbox at sandbox_root/w{wid}/ so each worker
    has its own state/budget/logs without clobbering anything else.
    """
    worker_dir = sandbox_root / f"w{wid}"
    worker_dir.mkdir(parents=True, exist_ok=True)
    (worker_dir / "logs").mkdir(exist_ok=True)
    (worker_dir / "manifests").mkdir(exist_ok=True)
    (worker_dir / "attempts").mkdir(exist_ok=True)
    (worker_dir / "solutions").mkdir(exist_ok=True)
    (worker_dir / "failed").mkdir(exist_ok=True)

    # Stage the repos dir — point at the real one read-only via symlink
    repos_dir = worker_dir / "repos"
    repos_dir.mkdir(exist_ok=True)
    ttp_link = repos_dir / "toke-test-programs"
    if not ttp_link.exists():
        ttp_link.symlink_to(BASE)
    toke_link = repos_dir / "toke"
    if not toke_link.exists() and (BASE.parent / "toke").exists():
        toke_link.symlink_to(BASE.parent / "toke")

    # Stage the manifest into the worker's manifests dir
    staged_manifest = worker_dir / "manifests" / f"w{wid}.json"
    shutil.copy(manifest, staged_manifest)

    # Copy repair-hints + held-list + audit-report so the worker can read them
    for fname in ("repair-hints.json", "held-programs.json", "audit-report.json"):
        src = BASE / "results" / fname
        if src.exists():
            (worker_dir / "repos" / "toke-test-programs" / "results").mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    env.update({
        "DRY_RUN": "1",
        "WORKER_ID": str(wid),
        "TOTAL_WORKERS": "5",
        "WORKER_DIR": str(worker_dir),
        "MANIFEST_PATH": str(staged_manifest),
        "BUDGET_USD_CAP": "5.0",
        "MAX_OPUS_ITERATIONS": "1",
        "MAX_SONNET_ITERATIONS": "0",
        "USE_TOKE_API": "0",
        "RUN_MODE": "manifest",
        "ANTHROPIC_API_KEY": "dryrun-no-real-key",
        "TKC": TKC,
        "TKC_STDLIB_DIR": f"{BASE.parent}/toke/src/stdlib",  # for tkc on Mac
    })

    log_file = worker_dir / "logs" / "dry-run.log"
    try:
        proc = subprocess.run(
            [sys.executable, str(WORKER_SCRIPT)],
            env=env,
            capture_output=True, text=True, timeout=300,
            errors="replace",
        )
        log_file.write_text(proc.stdout + "\n--- STDERR ---\n" + proc.stderr)
        return {
            "wid": wid,
            "returncode": proc.returncode,
            "log": str(log_file),
            "manifest": str(manifest),
        }
    except subprocess.TimeoutExpired:
        return {"wid": wid, "returncode": -1, "log": str(log_file), "error": "TIMEOUT 5min"}
    except Exception as e:
        return {"wid": wid, "returncode": -2, "log": str(log_file), "error": str(e)}


def summarize(results: list[dict], sandbox_root: Path) -> int:
    """Print per-worker summary; return 0 if all clean, 1 otherwise."""
    print("\n" + "=" * 70)
    print("DRY-RUN SUMMARY")
    print("=" * 70)
    any_bad = False
    for r in sorted(results, key=lambda x: x["wid"]):
        wid = r["wid"]
        rc = r["returncode"]
        worker_dir = sandbox_root / f"w{wid}"
        state_file = worker_dir / "state-dryrun.json"
        budget_file = worker_dir / "budget-dryrun.json"

        line = f"w{wid}: rc={rc}"
        if rc != 0:
            line += f"  CRASH (see {r['log']})"
            any_bad = True
        else:
            # Parse state for counts
            if state_file.exists():
                s = json.loads(state_file.read_text())
                done = len(s.get("completed", []))
                failed = len(s.get("failed", []))
                skipped = len(s.get("skipped", []))
                line += f"  done={done} fail={failed} skip={skipped}"
            else:
                line += f"  no state file produced"
                any_bad = True
            if budget_file.exists():
                b = json.loads(budget_file.read_text())
                line += f"  spend=${b.get('usd_spent', 0):.2f}"
                if b.get("usd_spent", 0) > 0.01:
                    line += "  ⚠️  NON-ZERO SPEND IN DRY RUN!"
                    any_bad = True
            else:
                line += "  no budget file"
        print(f"  {line}")
    print("=" * 70)
    return 0 if not any_bad else 1


def main():
    p = argparse.ArgumentParser()
    p.add_argument("manifest_dir", nargs="?", default=str(DEFAULT_MANIFEST_DIR))
    p.add_argument("--workers", type=int, default=5)
    p.add_argument("--keep-sandbox", action="store_true",
                   help="Don't delete the temp sandbox after run (for debugging)")
    args = p.parse_args()

    manifest_dir = Path(args.manifest_dir)
    if not manifest_dir.is_dir():
        print(f"manifest dir not found: {manifest_dir}", file=sys.stderr)
        sys.exit(2)

    # Find each worker's manifest
    manifests = {}
    for wid in range(1, args.workers + 1):
        m = find_manifest(manifest_dir, wid)
        if not m:
            print(f"no manifest for w{wid} in {manifest_dir}", file=sys.stderr)
            sys.exit(2)
        manifests[wid] = m
        print(f"w{wid} → {m.name}")

    sandbox = Path(tempfile.mkdtemp(prefix="toke-dryrun-"))
    print(f"\nsandbox: {sandbox}")

    # Run workers in parallel via concurrent.futures
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futures = [ex.submit(run_one_worker, wid, m, sandbox) for wid, m in manifests.items()]
        results = [f.result() for f in futures]

    rc = summarize(results, sandbox)
    if args.keep_sandbox:
        print(f"\nsandbox preserved at: {sandbox}")
    else:
        shutil.rmtree(sandbox, ignore_errors=True)
    sys.exit(rc)


if __name__ == "__main__":
    main()
