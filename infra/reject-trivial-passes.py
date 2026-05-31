#!/usr/bin/env python3
"""reject-trivial-passes.py — remove `solution.tk` files for programs the
post-R5 audit flagged as trivial passes (the model just hardcoded the literal
expected_output without doing the real algorithm).

Trivial cases identified in 107.R5 (commit pending):
  - NET-162 (just io.println("Sent"))
  - NET-183 (just io.println("Replaying"))
  - SEC-070 (94 bytes, no logic)
  - CRY-035 (placeholder expected_output)
  - NET-136 (both if/el branches print same literal)
  - NET-166 (always prints "SERVING")
  - NET-200 (all functions stub-return constants)
  - SYS-108 (prints literal labels, no netstat)

Action per program:
  - Move solution.tk → solution.trivial-rejected-by-R6.tk (keep for forensics)
  - Move status.json → status.trivial-rejected-by-R6.json
  - Log to results/107-R5/trivial-rejected.json with verdict + reason

These specs ALSO need hardening (R6 follow-up) because they admit hardcoded
constants as valid solutions. See scan-trivial-prone-specs.py.

Story 107.R6.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SOLUTIONS = BASE / "results" / "solutions"

TRIVIAL = [
    ("NET-162", "networking-rest", "io.println('Sent') — ignores all 4 stdin inputs (URL/secret/file/conc), no HTTP signing"),
    ("NET-183", "networking-rest", "io.println('Replaying') — no actual replay logic"),
    ("SEC-070", "security", "94-byte program with no logic"),
    ("CRY-035", "crypto-blockchain", "echoes spec's placeholder 'shared_secret_hex' — spec is broken"),
    ("NET-136", "networking-rest", "if/el branches both print 'BREAKING CHANGES' — no real diffing"),
    ("NET-166", "networking-rest", "always prints 'SERVING' for any non-empty input — no real gRPC"),
    ("NET-200", "networking-rest", "all service functions stub-return constants — runtest always true"),
    ("SYS-108", "system-tools", "prints literal labels '(listening TCP sockets)' / '(all TCP connections)' — no netstat"),
]


def main():
    rejected = []
    now = datetime.now(timezone.utc).isoformat()
    for pid, cat, reason in TRIVIAL:
        prog_dir = SOLUTIONS / cat / pid
        sol = prog_dir / "solution.tk"
        status = prog_dir / "status.json"
        if not sol.exists():
            print(f"  {pid}: no solution.tk to reject (skipping)")
            continue
        backup = prog_dir / "solution.trivial-rejected-by-R6.tk"
        sol.rename(backup)
        if status.exists():
            status.rename(prog_dir / "status.trivial-rejected-by-R6.json")
        rejected.append({"id": pid, "category": cat, "reason": reason, "rejected_at": now})
        print(f"  {pid:<10} [{cat:<20}] REJECTED — {reason[:60]}")

    out = BASE / "results" / "107-R5" / "trivial-rejected.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"rejected": rejected, "story": "107.R6"}, indent=2))
    print(f"\nRejected {len(rejected)} trivial passes; log at {out}")


if __name__ == "__main__":
    main()
