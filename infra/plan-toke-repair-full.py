#!/usr/bin/env python3
"""plan-toke-repair-full.py — manifest for the full eligible pool.

Eligibility (same gates as plan-toke-repair-sample-50.py):
  - python ref status = PASS
  - toke status != PASS
  - NOT in held-programs.json (catches disabled-in-spec + python-not-passing)
  - has a toke source on disk

Round-robin across 5 workers. Each entry carries id/category/status/error_codes
/hint/source — same shape the worker manifest_iteration consumes.

Per-program override fields baked in: model=opus, max_opus=N (default 3),
max_sonnet=0, mode=repair. Set MAX_OPUS env to override.

Story 107.R3.
"""

import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
CATEGORIES = BASE / "categories"
PY_REFS = BASE / "results" / "python-refs"
SOLUTIONS = BASE / "results" / "solutions"
AUDIT = BASE / "results" / "audit-report.json"
HINTS = BASE / "results" / "repair-hints.json"
HELD = BASE / "results" / "held-programs.json"
TAGS_OUT = BASE / "results" / "tagged-toke-repair-full.json"
MANIFEST_DIR = BASE / "infra" / "manifests-py-repair"
NUM_WORKERS = 5
MAX_OPUS = int(os.environ.get("MAX_OPUS", "3"))


def main():
    audit = json.loads(AUDIT.read_text())
    hints = json.loads(HINTS.read_text())
    held = {p["id"] for p in json.loads(HELD.read_text())["programs"]}

    eligible = []
    skipped = defaultdict(int)
    for prog in audit["programs"]:
        pid = prog["id"]
        if pid in held:
            skipped["in_held"] += 1
            continue
        if prog.get("status") == "PASS":
            skipped["toke_already_pass"] += 1
            continue
        cat = prog["category"]
        if not (SOLUTIONS / cat / pid / "solution.tk").exists():
            skipped["no_toke_source"] += 1
            continue
        py_status_file = PY_REFS / cat / pid / "status.json"
        if not py_status_file.exists():
            skipped["no_python_status"] += 1
            continue
        try:
            if json.loads(py_status_file.read_text()).get("status") != "PASS":
                skipped["python_not_passing"] += 1
                continue
        except Exception:
            skipped["python_parse_err"] += 1
            continue
        eligible.append(prog)

    print(f"Audit programs: {len(audit['programs'])}")
    for k, v in skipped.items():
        print(f"  skipped — {k}: {v}")
    print(f"ELIGIBLE: {len(eligible)}")

    # ----------------------------------------------------------------------
    # 107.R4.3: STRATIFIED distribution — group by category, shuffle within
    # each, round-robin across workers, interleave so workers see a mixed
    # category sequence from the start of their queue.
    # ----------------------------------------------------------------------
    import random as _random
    STRATIFY_SEED = int(os.environ.get("STRATIFY_SEED", "107"))
    rng = _random.Random(STRATIFY_SEED)

    by_cat: dict[str, list] = defaultdict(list)
    for p in eligible:
        by_cat[p["category"]].append(p)

    # Sort programs within each category for determinism, then shuffle with the seed
    for cat in by_cat:
        by_cat[cat].sort(key=lambda p: p["id"])
        rng.shuffle(by_cat[cat])

    # Round-robin within each category (so distribution is balanced per-cat)
    cat_worker_queues: dict[str, dict[int, list]] = defaultdict(lambda: defaultdict(list))
    for cat, progs in by_cat.items():
        for i, prog in enumerate(progs):
            wid = (i % NUM_WORKERS) + 1
            cat_worker_queues[cat][wid].append(prog)

    # Interleave categories within each worker's manifest so the FIRST few
    # programs span multiple categories (early-abort signal works correctly,
    # and a budget-hit doesn't leave one category over-represented in fails).
    buckets: dict[int, list] = defaultdict(list)
    cat_order = sorted(by_cat.keys())  # deterministic
    while True:
        any_added = False
        for cat in cat_order:
            for wid in range(1, NUM_WORKERS + 1):
                q = cat_worker_queues[cat][wid]
                if q:
                    buckets[wid].append(q.pop(0))
                    any_added = True
        if not any_added:
            break

    # Build manifest entries
    for wid in range(1, NUM_WORKERS + 1):
        enriched = []
        for prog in buckets[wid]:
            pid = prog["id"]
            cat = prog["category"]
            src = (SOLUTIONS / cat / pid / "solution.tk").read_text(errors="replace")
            if pid not in hints:
                print(f"  WARN: {pid} missing from repair-hints.json", file=sys.stderr)
                hint_text = "(no targeted hint)"
            else:
                h = hints[pid]
                hint_text = " | ".join(h.get("hints", [])) or "(no targeted hint)"
            enriched.append({
                "id": pid,
                "category": cat,
                "status": prog.get("status"),
                "error_codes": prog.get("error_codes", []),
                "hint": hint_text,
                "source": src,
                "mode": "repair",
                "model": "opus",
                "max_iterations": MAX_OPUS,
                "max_opus": MAX_OPUS,
                "max_sonnet": 0,
            })
        buckets[wid] = enriched

    # ----------------------------------------------------------------------
    # 107.R4.2: DISTRIBUTION VALIDATION — refuse to write manifests if any
    # worker is lopsided. Allow override via --allow-skew flag.
    # ----------------------------------------------------------------------
    allow_skew = "--allow-skew" in sys.argv
    mean_size = len(eligible) / NUM_WORKERS

    # Per-worker × per-category matrix
    matrix: dict[int, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for wid in range(1, NUM_WORKERS + 1):
        for p in buckets[wid]:
            matrix[wid][p["category"]] += 1

    # Print matrix
    all_cats_sorted = sorted({c for w in matrix.values() for c in w})
    print(f"\n=== Per-worker × per-category matrix (mean size {mean_size:.1f}) ===")
    header = "  " + "wid".ljust(4) + "size".rjust(6) + "".join(c[:8].rjust(10) for c in all_cats_sorted)
    print(header)
    for wid in range(1, NUM_WORKERS + 1):
        size = len(buckets[wid])
        row = "  " + f"w{wid}".ljust(4) + str(size).rjust(6)
        for c in all_cats_sorted:
            n = matrix[wid].get(c, 0)
            row += str(n).rjust(10)
        print(row)

    # Validate — tolerance accommodates natural rounding from stratified round-robin
    # across 15 categories (~5% of mean is reasonable).
    size_tol = max(5, int(mean_size * 0.05))
    violations = []
    for wid in range(1, NUM_WORKERS + 1):
        progs = buckets[wid]
        if not progs:
            continue
        size_dev = abs(len(progs) - mean_size)
        if size_dev > size_tol:
            violations.append(f"w{wid}: size {len(progs)} differs by {size_dev:.1f} from mean (>±{size_tol})")
        for cat, n in matrix[wid].items():
            pct = n / len(progs) * 100
            if pct > 40:
                violations.append(f"w{wid}: '{cat}' is {pct:.1f}% of load ({n}/{len(progs)}) — exceeds 40%")
    if violations:
        print("\n=== DISTRIBUTION VIOLATIONS ===", file=sys.stderr)
        for v in violations:
            print(f"  ❌ {v}", file=sys.stderr)
        if not allow_skew:
            print("\nRefusing to write manifests. Pass --allow-skew to override.", file=sys.stderr)
            sys.exit(2)
        print("\n--allow-skew set; writing manifests despite violations.", file=sys.stderr)

    # Tag file
    TAGS_OUT.write_text(json.dumps({
        "story": f"107.R4: full repair sweep, {MAX_OPUS} Opus attempts, $10/worker, stratified seed={STRATIFY_SEED}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "stratify_seed": STRATIFY_SEED,
        "total": len(eligible),
        "tags": [
            {"id": p["id"], "category": p["category"], "status": p["status"], "worker_id": wid}
            for wid in range(1, NUM_WORKERS + 1) for p in buckets[wid]
        ],
    }, indent=2))

    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()
    for wid in range(1, NUM_WORKERS + 1):
        progs = buckets[wid]
        manifest = {
            "story": f"107.R4: full repair sweep, {MAX_OPUS} Opus attempts, $10/worker, stratified",
            "worker_id": wid,
            "generated_at": now,
            "stratify_seed": STRATIFY_SEED,
            "mode": "manifest",
            "total": len(progs),
            "programs": progs,
        }
        (MANIFEST_DIR / f"w{wid}-full.json").write_text(json.dumps(manifest, indent=2))

    print(f"\nWrote {NUM_WORKERS} manifests to {MANIFEST_DIR}/")


if __name__ == "__main__":
    main()
