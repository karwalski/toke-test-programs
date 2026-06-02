#!/usr/bin/env python3
"""regen-held-list-post-107-R1.py — rebuild held-programs.json to reflect
the post-107.R1 state of the corpus.

A program should be HELD if:
  1. `disabled: true` in requirements.yaml (spec deemed unfixable), OR
  2. python ref doesn't PASS (no status.json, status != PASS — meaning the
     reference can't validate toke output).

Both reasons live in the same list so the orchestrator's single filter applies.
Each entry carries `reason` so we know why it's held.

Output: results/held-programs.json (overwrites).

Story 107.R1 follow-up.
"""

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from collections import Counter

BASE = Path(__file__).resolve().parent.parent
CATEGORIES = BASE / "categories"
PY_REFS = BASE / "results" / "python-refs"
HELD = BASE / "results" / "held-programs.json"


def find_program_ids_and_disabled() -> tuple[dict, set]:
    """Return ({id: category}, {disabled_ids}) via tolerant line-level scan."""
    ids = {}
    disabled = set()
    for req in CATEGORIES.glob("*/requirements.yaml"):
        cat = req.parent.name
        cur_id = None
        for line in req.read_text(errors="replace").split("\n"):
            m = re.match(r'^- id:\s*["\']?([A-Z]+-\d+)["\']?\s*$', line)
            if m:
                cur_id = m.group(1)
                ids[cur_id] = cat
                continue
            if cur_id and re.match(r'^\s+disabled:\s*true\b', line):
                disabled.add(cur_id)
    return ids, disabled


def python_status(category: str, prog_id: str) -> str:
    """Return PASS / NON_PASS / NO_REF based on results/python-refs/<cat>/<id>/status.json."""
    p = PY_REFS / category / prog_id / "status.json"
    if not p.exists():
        return "NO_REF"
    try:
        d = json.loads(p.read_text())
        return "PASS" if d.get("status") == "PASS" else "NON_PASS"
    except Exception:
        return "NON_PASS"


def main():
    ids, disabled = find_program_ids_and_disabled()
    print(f"Corpus: {len(ids)} programs ({len(disabled)} disabled)")

    held = []
    reason_counts = Counter()
    for pid, cat in ids.items():
        if pid in disabled:
            held.append({"id": pid, "category": cat, "reason": "disabled_in_spec"})
            reason_counts["disabled_in_spec"] += 1
            continue
        py = python_status(cat, pid)
        if py == "NO_REF":
            held.append({"id": pid, "category": cat, "reason": "no_python_ref"})
            reason_counts["no_python_ref"] += 1
        elif py == "NON_PASS":
            held.append({"id": pid, "category": cat, "reason": "python_ref_not_passing"})
            reason_counts["python_ref_not_passing"] += 1

    out = {
        "epic": "107.R1 follow-up — regenerated post Python repair sweep",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "rationale": (
            "A program is held if either (a) its spec is `disabled: true` in "
            "requirements.yaml, or (b) its Python reference does not PASS — "
            "meaning we cannot validate toke output against it. The repair "
            "loop should skip held programs in both cases."
        ),
        "total_held": len(held),
        "programs": held,
    }
    HELD.write_text(json.dumps(out, indent=2))

    print(f"Held now: {len(held)}")
    for r, n in reason_counts.most_common():
        print(f"  {r}: {n}")
    print(f"Active (eligible for repair): {len(ids) - len(held)}")


if __name__ == "__main__":
    main()
