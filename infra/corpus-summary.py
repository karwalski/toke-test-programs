#!/usr/bin/env python3
"""corpus-summary.py — produce a status × python/toke breakdown of the whole
corpus from per-program status.json + the disabled flag in requirements.yaml.

No new audit run — derives everything from on-disk artefacts.

Output columns:
  status   — one of {PASS, WRONG_OUTPUT, RUN_FAIL, BUILD_FAIL, COMPILE_FAIL,
             TIMEOUT, SEGFAULT, DISABLED, NO_REF, …}
  python   — # programs whose results/python-refs/<cat>/<id>/status.json
             reports that status
  toke     — # programs whose results/solutions/<cat>/<id>/status.json
             OR results/failed/<cat>/<id>/status.json reports that status
  total    — # programs across the corpus with that classification on either
             side (union, deduped by id)

DISABLED is special: counted separately (from requirements.yaml `disabled: true`)
and excluded from other buckets.
"""

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
CATEGORIES = BASE / "categories"
PY_REFS = BASE / "results" / "python-refs"
TOKE_AUDIT = BASE / "results" / "audit-report.json"


def find_program_ids() -> dict:
    """Return {id: category} by scanning requirements.yaml files with a
    tolerant line-level parser (avoids YAML errors on rare binary outputs)."""
    ids = {}
    disabled = set()
    for req in CATEGORIES.glob("*/requirements.yaml"):
        cat = req.parent.name
        cur_id = None
        in_entry_after_id = False
        for line in req.read_text(errors="replace").split("\n"):
            m = re.match(r'^- id:\s*["\']?([A-Z]+-\d+)["\']?\s*$', line)
            if m:
                cur_id = m.group(1)
                ids[cur_id] = cat
                in_entry_after_id = True
                continue
            if in_entry_after_id and cur_id and re.match(r'^\s+disabled:\s*true\b', line):
                disabled.add(cur_id)
    return ids, disabled


def read_status(path: Path) -> str | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text()).get("status")
    except Exception:
        return "PARSE_ERR"


def main():
    ids, disabled = find_program_ids()
    print(f"Programs in corpus: {len(ids)}")
    print(f"Disabled (per requirements.yaml): {len(disabled)}")
    print()

    # Load Toke statuses from the canonical audit-report.json
    toke_status = {}
    audit = json.loads(TOKE_AUDIT.read_text())
    for prog in audit.get("programs", []):
        toke_status[prog["id"]] = prog.get("status", "UNKNOWN")
    print(f"Toke statuses from audit-report.json ({audit.get('timestamp','?')}, tkc {audit.get('tkc_version','?')}): {len(toke_status)} programs")
    print()

    py = {}    # id -> status
    toke = {}  # id -> status
    for pid, cat in ids.items():
        if pid in disabled:
            py[pid] = "DISABLED"
            toke[pid] = "DISABLED"
            continue
        # Python ref status
        st = read_status(PY_REFS / cat / pid / "status.json")
        py[pid] = st if st else "NO_REF"
        # Toke status from audit
        toke[pid] = toke_status.get(pid, "NO_REF")

    # Union of statuses
    all_statuses = sorted(set(py.values()) | set(toke.values()))
    py_counter = Counter(py.values())
    toke_counter = Counter(toke.values())

    # Total = # programs (deduped by id) classified into this status by *either* side
    total_per_status = {}
    for s in all_statuses:
        total_per_status[s] = sum(1 for pid in ids if py[pid] == s or toke[pid] == s)

    # Pretty table
    print(f"{'status':<18} {'python':>8} {'toke':>8} {'total':>8}")
    print("-" * 50)
    # Sort: DISABLED first, then PASS, then alphabetical
    order_key = lambda s: (0 if s == "DISABLED" else 1 if s == "PASS" else 2, s)
    for s in sorted(all_statuses, key=order_key):
        print(f"{s:<18} {py_counter.get(s,0):>8} {toke_counter.get(s,0):>8} {total_per_status[s]:>8}")
    print("-" * 50)
    print(f"{'CORPUS_TOTAL':<18} {sum(py_counter.values()):>8} {sum(toke_counter.values()):>8} {len(ids):>8}")


if __name__ == "__main__":
    main()
