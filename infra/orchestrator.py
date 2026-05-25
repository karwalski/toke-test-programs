#!/usr/bin/env python3
"""orchestrator.py — Local monitoring and control script for toke generation workers.

Runs on your machine. SSHes to each worker to read state, report progress,
detect stuck workers, and trigger actions.

Usage:
    python3 orchestrator.py status          # Show all worker statuses
    python3 orchestrator.py start           # Start worker service on all
    python3 orchestrator.py stop            # Stop worker service on all
    python3 orchestrator.py start 3         # Start worker 3 only
    python3 orchestrator.py collect         # Trigger collect-results.sh
    python3 orchestrator.py watch           # Continuous monitoring (Ctrl+C to stop)
"""

import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# --- Configuration ---
# Worker IPs are read from workers.json (created by launch-workers.sh)
WORKERS_FILE = Path(__file__).parent / "workers.json"
SSH_KEY = Path.home() / ".ssh" / "toke-workers.pem"
SSH_USER = "ubuntu"
SSH_OPTS = [
    "-o", "StrictHostKeyChecking=no",
    "-o", "ConnectTimeout=10",
    "-o", "BatchMode=yes",
    "-i", str(SSH_KEY),
]

STUCK_THRESHOLD_MINUTES = 10


def load_workers() -> dict[int, str]:
    """Load worker ID -> IP mapping from workers.json."""
    if not WORKERS_FILE.exists():
        print(f"ERROR: {WORKERS_FILE} not found.")
        print("Run launch-workers.sh first, or create workers.json manually:")
        print('  {"1": "1.2.3.4", "2": "5.6.7.8", ...}')
        sys.exit(1)

    with open(WORKERS_FILE) as f:
        data = json.load(f)
    return {int(k): v for k, v in data.items()}


def ssh_cmd(ip: str, command: str) -> tuple[int, str]:
    """Execute a command on a remote worker via SSH."""
    full_cmd = ["ssh"] + SSH_OPTS + [f"{SSH_USER}@{ip}", command]
    try:
        result = subprocess.run(
            full_cmd, capture_output=True, text=True, timeout=30
        )
        return result.returncode, (result.stdout + result.stderr).strip()
    except subprocess.TimeoutExpired:
        return -1, "SSH timeout"
    except Exception as e:
        return -1, str(e)


def get_worker_state(ip: str) -> dict | None:
    """Read state.json from a worker."""
    rc, output = ssh_cmd(ip, "cat /opt/toke-worker/state.json 2>/dev/null")
    if rc == 0 and output:
        try:
            return json.loads(output)
        except json.JSONDecodeError:
            return None
    return None


def format_duration(seconds: float) -> str:
    """Format seconds into human-readable duration."""
    if seconds < 60:
        return f"{seconds:.0f}s"
    elif seconds < 3600:
        return f"{seconds/60:.1f}m"
    else:
        return f"{seconds/3600:.1f}h"


def cmd_status(workers: dict[int, str], specific_worker: int | None = None):
    """Show status of all (or one) workers."""
    total_completed = 0
    total_failed = 0
    total_skipped = 0
    total_in_progress = 0

    targets = {specific_worker: workers[specific_worker]} if specific_worker else workers

    print(f"\n{'='*70}")
    print(f"  TOKE WORKER STATUS  —  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}\n")

    for wid, ip in sorted(targets.items()):
        state = get_worker_state(ip)
        if state is None:
            print(f"  Worker {wid} ({ip}):  UNREACHABLE / NO STATE")
            continue

        completed = len(state.get("completed", []))
        failed = len(state.get("failed", []))
        skipped = len(state.get("skipped", []))
        in_progress = state.get("in_progress")
        last_updated = state.get("last_updated")

        total_completed += completed
        total_failed += failed
        total_skipped += skipped

        # Check if stuck
        stuck = ""
        if last_updated and in_progress:
            last_dt = datetime.fromisoformat(last_updated)
            age_min = (datetime.now(timezone.utc) - last_dt).total_seconds() / 60
            if age_min > STUCK_THRESHOLD_MINUTES:
                stuck = f"  *** STUCK ({age_min:.0f}m) ***"

        if in_progress:
            total_in_progress += 1

        status_line = (
            f"  Worker {wid} ({ip}):  "
            f"done={completed}  failed={failed}  skipped={skipped}  "
            f"current={in_progress or '-'}{stuck}"
        )
        print(status_line)

        if last_updated:
            print(f"    Last update: {last_updated}")

    print(f"\n{'─'*70}")
    print(
        f"  TOTALS:  completed={total_completed}  failed={total_failed}  "
        f"skipped={total_skipped}  in_progress={total_in_progress}"
    )
    overall = total_completed + total_failed + total_skipped
    print(f"  Processed: {overall} total")
    print(f"{'='*70}\n")


def cmd_start(workers: dict[int, str], specific_worker: int | None = None):
    """Start the worker service."""
    targets = {specific_worker: workers[specific_worker]} if specific_worker else workers
    for wid, ip in sorted(targets.items()):
        print(f"  Starting worker {wid} ({ip})... ", end="")
        rc, output = ssh_cmd(ip, "sudo systemctl start toke-worker")
        print("OK" if rc == 0 else f"FAILED: {output}")


def cmd_stop(workers: dict[int, str], specific_worker: int | None = None):
    """Stop the worker service."""
    targets = {specific_worker: workers[specific_worker]} if specific_worker else workers
    for wid, ip in sorted(targets.items()):
        print(f"  Stopping worker {wid} ({ip})... ", end="")
        rc, output = ssh_cmd(ip, "sudo systemctl stop toke-worker")
        print("OK" if rc == 0 else f"FAILED: {output}")


def cmd_watch(workers: dict[int, str]):
    """Continuous monitoring loop."""
    print("Watching workers (Ctrl+C to stop)...\n")
    try:
        while True:
            cmd_status(workers)
            time.sleep(60)
    except KeyboardInterrupt:
        print("\nStopped.")


def cmd_collect():
    """Run collect-results.sh."""
    script = Path(__file__).parent / "collect-results.sh"
    if not script.exists():
        print(f"ERROR: {script} not found")
        sys.exit(1)
    subprocess.run(["bash", str(script)])


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]
    specific_worker = int(sys.argv[2]) if len(sys.argv) > 2 else None

    workers = load_workers()

    if specific_worker and specific_worker not in workers:
        print(f"ERROR: Worker {specific_worker} not found in workers.json")
        sys.exit(1)

    if command == "status":
        cmd_status(workers, specific_worker)
    elif command == "start":
        cmd_start(workers, specific_worker)
    elif command == "stop":
        cmd_stop(workers, specific_worker)
    elif command == "watch":
        cmd_watch(workers)
    elif command == "collect":
        cmd_collect()
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
