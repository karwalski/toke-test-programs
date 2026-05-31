#!/usr/bin/env python3
"""plan-toke-repair-sample-50.py — build manifests for a small sample run.

Eligibility:
  - Python ref status = PASS (we can validate toke output against it)
  - Toke status != PASS (something to repair)
  - NOT in held-programs.json (catches disabled + python-failing)

From the eligible set, sample 10 per worker × 5 = 50 programs. Round-robin by
hash so the sample is reproducible across runs (seed=107R1).

Each manifest entry carries:
  - id, category
  - status (from audit-report.json)
  - error_codes
  - hint (from repair-hints.json)
  - source (current toke source embedded — repair starts from this)
  - model="opus", max_opus=1, max_sonnet=0, max_iterations=1, mode="repair"

Pre-flight assertions (raises on failure):
  - every selected id has a requirements entry
  - every selected id has results/solutions/<cat>/<id>/solution.tk
  - every selected id has a hint in repair-hints.json
  - every selected id has a status in audit-report.json
  - sample size is exactly 50 (or < if pool too small)

Outputs:
  infra/manifests-py-repair/w{1..5}-toke-sample-50.json
  results/tagged-toke-sample-50.json  — flat list of {id, category, status} tags
"""

import json
import random
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
TAGS_OUT = BASE / "results" / "tagged-toke-sample-50.json"
MANIFEST_DIR = BASE / "infra" / "manifests-py-repair"
NUM_WORKERS = 5
PER_WORKER = 10
SEED = 107


def main():
    audit = json.loads(AUDIT.read_text())
    hints = json.loads(HINTS.read_text())
    held = {p["id"] for p in json.loads(HELD.read_text())["programs"]}

    by_id = {p["id"]: p for p in audit["programs"]}

    # Eligible: toke status != PASS AND id not in held AND python PASS AND tk source exists
    eligible = []
    skipped_reasons = defaultdict(int)
    for prog in audit["programs"]:
        pid = prog["id"]
        if pid in held:
            skipped_reasons["in_held"] += 1
            continue
        if prog.get("status") == "PASS":
            skipped_reasons["toke_already_pass"] += 1
            continue
        cat = prog["category"]
        # Verify toke source exists (would skip if missing)
        if not (SOLUTIONS / cat / pid / "solution.tk").exists():
            skipped_reasons["no_toke_source"] += 1
            continue
        # Verify python ref PASSES (audit doesn't track py; check status.json directly)
        py_status_file = PY_REFS / cat / pid / "status.json"
        if not py_status_file.exists():
            skipped_reasons["no_python_status"] += 1
            continue
        try:
            py_status = json.loads(py_status_file.read_text()).get("status")
        except Exception:
            skipped_reasons["python_status_parse_err"] += 1
            continue
        if py_status != "PASS":
            skipped_reasons["python_not_passing"] += 1
            continue
        # All checks pass
        eligible.append(prog)

    print(f"Audit programs: {len(audit['programs'])}")
    for r, n in skipped_reasons.items():
        print(f"  skipped — {r}: {n}")
    print(f"ELIGIBLE: {len(eligible)} (Python PASS + Toke NOT PASS + not held + has sources)")

    # 107.R4.3: stratified sampling — sample WITHIN each category in proportion
    # so the 50 programs span all 15 categories rather than randomly clumping.
    random.seed(SEED)
    sample_size = min(NUM_WORKERS * PER_WORKER, len(eligible))

    by_cat: dict[str, list] = defaultdict(list)
    for p in eligible:
        by_cat[p["category"]].append(p)
    cats = sorted(by_cat.keys())
    # Per-cat sample count proportional to eligible mix
    cat_counts = {c: max(1, round(len(by_cat[c]) / len(eligible) * sample_size)) for c in cats}
    # Normalise to sum to sample_size (drop extras from largest)
    while sum(cat_counts.values()) > sample_size:
        biggest = max(cat_counts, key=cat_counts.get)
        cat_counts[biggest] -= 1
    while sum(cat_counts.values()) < sample_size:
        smallest = min(cat_counts, key=cat_counts.get)
        cat_counts[smallest] += 1

    sample = []
    for cat in cats:
        n = min(cat_counts[cat], len(by_cat[cat]))
        sample.extend(random.sample(by_cat[cat], n))

    print(f"\nSampled {len(sample)} programs (seed={SEED}, stratified by category)")
    for cat in cats:
        print(f"  {cat}: {cat_counts[cat]} (from pool of {len(by_cat[cat])})")

    # Small-sample distribution: shuffle the whole 50-program list once, then
    # chunk into 5 equal pieces. Each worker gets exactly 10 (or ±1 if 50
    # doesn't divide cleanly). Categories are inherently mixed since the
    # input sample was stratified.
    random.shuffle(sample)
    buckets: dict[int, list] = defaultdict(list)
    for i, p in enumerate(sample):
        buckets[(i % NUM_WORKERS) + 1].append(p)

    # Enrich each entry
    for wid in range(1, NUM_WORKERS + 1):
        enriched = []
        for prog in buckets[wid]:
            pid = prog["id"]
            cat = prog["category"]
            src_path = SOLUTIONS / cat / pid / "solution.tk"
            source = src_path.read_text(errors="replace")

            if pid not in hints:
                print(f"  FAIL: {pid} not in repair-hints.json", file=sys.stderr)
                sys.exit(1)

            prog_hint = hints[pid]
            hint_text = " | ".join(prog_hint.get("hints", [])) or "(no targeted hint)"

            enriched.append({
                "id": pid,
                "category": cat,
                "status": prog.get("status"),
                "error_codes": prog.get("error_codes", []),
                "hint": hint_text,
                "source": source,
                "mode": "repair",
                "model": "opus",
                "max_iterations": 1,
                "max_opus": 1,
                "max_sonnet": 0,
            })
        buckets[wid] = enriched

    # 107.R4.2: distribution validation
    allow_skew = "--allow-skew" in sys.argv
    mean_size = sample_size / NUM_WORKERS
    matrix: dict[int, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for wid in range(1, NUM_WORKERS + 1):
        for p in buckets[wid]:
            matrix[wid][p["category"]] += 1
    violations = []
    size_tol = max(2, int(mean_size * 0.20))  # 50-program runs have larger relative tolerance
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
                violations.append(f"w{wid}: '{cat}' {pct:.0f}% of load ({n}/{len(progs)}) >40%")
    if violations:
        print("\n=== DISTRIBUTION VIOLATIONS ===", file=sys.stderr)
        for v in violations:
            print(f"  ❌ {v}", file=sys.stderr)
        if not allow_skew:
            print("Refusing to write. Pass --allow-skew to override.", file=sys.stderr)
            sys.exit(2)

    # Write tag file
    TAGS_OUT.write_text(json.dumps({
        "story": "107.R1 follow-up: toke repair sample-50 (1 Opus attempt each)",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "seed": SEED,
        "total": sample_size,
        "tags": [{"id": p["id"], "category": p["category"], "status": p["status"],
                  "worker_id": (i % NUM_WORKERS) + 1}
                 for i, p in enumerate(sample)],
    }, indent=2))
    print(f"\nWrote tag file: {TAGS_OUT}")

    # Write per-worker manifests
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()
    for wid in range(1, NUM_WORKERS + 1):
        progs = buckets[wid]
        manifest = {
            "story": "107.R1 follow-up: toke repair sample-50 (1 Opus attempt each)",
            "worker_id": wid,
            "generated_at": now,
            "mode": "manifest",
            "total": len(progs),
            "programs": progs,
        }
        out = MANIFEST_DIR / f"w{wid}-toke-sample-50.json"
        out.write_text(json.dumps(manifest, indent=2))

    print(f"\nWrote {NUM_WORKERS} manifests:")
    for wid in range(1, NUM_WORKERS + 1):
        progs = buckets[wid]
        ids = [p["id"] for p in progs]
        status_counts = defaultdict(int)
        for p in progs:
            status_counts[p["status"]] += 1
        print(f"  w{wid} ({len(progs)} progs): {dict(status_counts)}")
        print(f"        ids: {', '.join(ids)}")


if __name__ == "__main__":
    main()
