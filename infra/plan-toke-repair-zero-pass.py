#!/usr/bin/env python3
"""plan-toke-repair-zero-pass.py — sample N programs from each ZERO-PASS
category for each worker.

Why: 107.R3 only touched ai-agents. Need first data on the 10 categories
that have ZERO toke passes today: crypto-blockchain, data-processing,
devtools, games, manufacturing-ml, media-content, messaging, networking-rest,
security, system-tools.

Per-worker: 2 programs × 10 categories = 20 programs.
Total: 20 × 5 workers = 100 programs (with deterministic non-overlap).

Each manifest entry carries: max_opus=2 (1 initial + 1 retry), max_sonnet=0,
model=opus, mode=repair, source embedded.

Story 107.R5.
"""

import json
import os
import random
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import yaml

BASE = Path(__file__).resolve().parent.parent
CATEGORIES = BASE / "categories"
PY_REFS = BASE / "results" / "python-refs"
SOLUTIONS = BASE / "results" / "solutions"
AUDIT = BASE / "results" / "audit-report.json"
HINTS = BASE / "results" / "repair-hints.json"
HELD = BASE / "results" / "held-programs.json"
TAGS_OUT = BASE / "results" / "tagged-toke-zero-pass.json"
MANIFEST_DIR = BASE / "infra" / "manifests-py-repair"
R3_STATES_DIR = BASE / "results" / "107-R3"
NUM_WORKERS = 5
PER_CATEGORY_PER_WORKER = 2
MAX_OPUS = 2  # 1 initial + 1 retry
SEED = int(os.environ.get("STRATIFY_SEED", "107"))


def load_disabled_ids() -> set[str]:
    disabled: set[str] = set()
    for req in CATEGORIES.glob("*/requirements.yaml"):
        try:
            specs = yaml.safe_load(req.read_text())
        except Exception:
            continue
        for s in specs or []:
            if s.get("disabled") is True and "id" in s:
                disabled.add(s["id"])
    return disabled


def main():
    audit = json.loads(AUDIT.read_text())
    hints = json.loads(HINTS.read_text())
    held = {p["id"] for p in json.loads(HELD.read_text())["programs"]}
    disabled_ids = load_disabled_ids()
    print(f"Disabled specs in corpus: {len(disabled_ids)}")

    # Overlay R3 results to get TRUE current toke status
    prog_status = {p["id"]: p["status"] for p in audit["programs"]}
    prog_cat = {p["id"]: p["category"] for p in audit["programs"]}
    if R3_STATES_DIR.exists():
        for w in range(1, 6):
            sf = R3_STATES_DIR / f"state-w{w}.json"
            if sf.exists():
                s = json.loads(sf.read_text())
                for pid in s.get("completed", []):
                    if pid in prog_status:
                        prog_status[pid] = "PASS"

    # Find zero-pass categories (effective, post-R3)
    cat_pass_counts: dict[str, int] = defaultdict(int)
    for pid, status in prog_status.items():
        if status == "PASS":
            cat_pass_counts[prog_cat[pid]] += 1
    all_cats = {prog_cat[p] for p in prog_status}
    zero_pass_cats = sorted(c for c in all_cats if cat_pass_counts[c] == 0)
    print(f"Zero-pass categories ({len(zero_pass_cats)}): {zero_pass_cats}")
    print(f"Pass counts (all cats): {dict(cat_pass_counts)}")

    # Eligible: in zero-pass cat AND not held AND not toke-pass AND has source AND python passes
    eligible_by_cat: dict[str, list] = defaultdict(list)
    skipped = defaultdict(int)
    for prog in audit["programs"]:
        pid = prog["id"]
        cat = prog["category"]
        if cat not in zero_pass_cats:
            skipped["not_zero_pass_cat"] += 1
            continue
        if pid in held:
            skipped["in_held"] += 1
            continue
        if pid in disabled_ids:
            skipped["disabled_spec"] += 1
            continue
        # Use effective status (audit + R3 overlay)
        if prog_status.get(pid) == "PASS":
            skipped["toke_pass_after_r3"] += 1
            continue
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
        eligible_by_cat[cat].append(prog)

    print(f"\nSkipped counts: {dict(skipped)}")
    print(f"\nEligible per zero-pass category:")
    for cat in zero_pass_cats:
        print(f"  {cat}: {len(eligible_by_cat[cat])}")

    # Verify we have enough programs per category for the per-worker × per-cat target
    needed_per_cat = NUM_WORKERS * PER_CATEGORY_PER_WORKER  # 10 programs per cat
    for cat in zero_pass_cats:
        if len(eligible_by_cat[cat]) < needed_per_cat:
            print(f"  WARN: {cat} has only {len(eligible_by_cat[cat])} eligible, need {needed_per_cat}", file=sys.stderr)

    # Sample: shuffle each cat with seed, take first (NUM_WORKERS × PER_CAT) programs,
    # distribute round-robin so each worker gets exactly PER_CAT of each cat
    rng = random.Random(SEED)
    buckets: dict[int, list] = defaultdict(list)
    sampled_total = 0
    for cat in zero_pass_cats:
        pool = list(eligible_by_cat[cat])
        rng.shuffle(pool)
        take = pool[: needed_per_cat]
        for i, prog in enumerate(take):
            wid = (i % NUM_WORKERS) + 1
            buckets[wid].append(prog)
        sampled_total += len(take)

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

    # Distribution check + matrix print
    matrix: dict[int, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for wid in range(1, NUM_WORKERS + 1):
        for p in buckets[wid]:
            matrix[wid][p["category"]] += 1
    print(f"\n=== Per-worker × per-category matrix ===")
    header = "  " + "wid".ljust(4) + "size".rjust(6) + "".join(c[:8].rjust(10) for c in zero_pass_cats)
    print(header)
    for wid in range(1, NUM_WORKERS + 1):
        size = len(buckets[wid])
        row = "  " + f"w{wid}".ljust(4) + str(size).rjust(6)
        for c in zero_pass_cats:
            row += str(matrix[wid].get(c, 0)).rjust(10)
        print(row)

    # Validation: every worker should have exactly PER_CAT of each zero-pass cat
    violations = []
    for wid in range(1, NUM_WORKERS + 1):
        for cat in zero_pass_cats:
            n = matrix[wid].get(cat, 0)
            if n != PER_CATEGORY_PER_WORKER and len(eligible_by_cat[cat]) >= needed_per_cat:
                violations.append(f"w{wid}/{cat}: got {n}, expected {PER_CATEGORY_PER_WORKER}")
    if violations:
        print("\n=== DISTRIBUTION VIOLATIONS ===", file=sys.stderr)
        for v in violations[:10]:
            print(f"  ❌ {v}", file=sys.stderr)
        if "--allow-skew" not in sys.argv:
            sys.exit(2)

    # Tag file
    TAGS_OUT.write_text(json.dumps({
        "story": "107.R5: zero-pass-cats sweep, 2/cat/worker, Opus 4.8, 1+1 attempts, $5/worker",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "stratify_seed": SEED,
        "total": sampled_total,
        "zero_pass_categories": zero_pass_cats,
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
            "story": "107.R5: zero-pass-cats sweep, 2/cat/worker, Opus 4.8",
            "worker_id": wid,
            "generated_at": now,
            "stratify_seed": SEED,
            "mode": "manifest",
            "total": len(progs),
            "programs": progs,
        }
        (MANIFEST_DIR / f"w{wid}-zero-pass.json").write_text(json.dumps(manifest, indent=2))

    print(f"\nWrote {NUM_WORKERS} manifests to {MANIFEST_DIR}/ (w*-zero-pass.json)")
    print(f"Tag file: {TAGS_OUT}")
    print(f"\nTotal programs sampled: {sampled_total} ({NUM_WORKERS * len(zero_pass_cats) * PER_CATEGORY_PER_WORKER} expected)")


if __name__ == "__main__":
    main()
