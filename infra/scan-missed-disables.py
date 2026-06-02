#!/usr/bin/env python3
"""scan-missed-disables.py — sweep all 2065 specs for keyword patterns that
signal "impossible in stdlib toke" and disable any that aren't already disabled.

Patterns:
  - requires-network: 'http get', 'http post', 'http request', 'httpbin',
                      'fetches', 'live api', 'rest endpoint', 'websocket'
  - requires-llm:     'llm', 'gpt', 'natural language understanding'
  - non-deterministic: 'monte carlo', 'simulation' (with random/agent/evolve),
                       'pheromone', 'random walk', 'random sample'

A spec is disabled if it matches AND is not already disabled. Existing
disabled programs are left untouched.

Story 107.R2 (follow-up to 107.R1 phase-1 disables).
"""

import json
import re
import sys
from datetime import date
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
CATEGORIES = BASE / "categories"

# (reason_tag, keyword_pattern, optional_context_pattern)
RULES = [
    # NETWORK
    ("requires-network", r"\bhttp(?:s)?(?:\s+(?:get|post|put|delete|request|client))?\b", None),
    ("requires-network", r"httpbin", None),
    ("requires-network", r"\bwebsocket\b", None),
    ("requires-network", r"\b(?:fetches?|fetch(?:ing)?)\s+(?:a|the|data|content)\b", None),
    ("requires-network", r"\brest\s+(?:endpoint|api|client)\b", None),
    ("requires-network", r"\blive\s+(?:api|http|service)\b", None),
    # LLM
    ("requires-llm", r"\bLLM\b", None),
    ("requires-llm", r"\bGPT\b", None),
    ("requires-llm", r"natural language understanding", None),
    ("requires-llm", r"semantic (?:scoring|similarity|relevance)", None),
    # NON-DETERMINISTIC
    ("non-deterministic", r"monte carlo", None),
    ("non-deterministic", r"pheromone", None),
    ("non-deterministic", r"random walk", None),
    ("non-deterministic", r"random sample", None),
    ("non-deterministic", r"\bsimulat(?:e|ion)\b.*\b(?:random|agent|evolv|pheromone)", None),
]


def classify_spec(desc: str) -> str | None:
    """Return the first matching reason tag, or None."""
    d = desc.lower()
    for reason, pat, ctx in RULES:
        if re.search(pat, d, re.IGNORECASE):
            return reason
    return None


def disable_in_file(req_path: Path, target_id: str, reason: str, today: str) -> bool:
    """Same line-level insert as apply-107-R1-disables.py. Idempotent."""
    text = req_path.read_text()
    lines = text.split("\n")
    out = []
    i = 0
    edited = False
    while i < len(lines):
        line = lines[i]
        out.append(line)
        m = re.match(r'^- id:\s*["\']?([A-Z]+-\d+)["\']?\s*$', line)
        if m and m.group(1) == target_id:
            # Already disabled?
            if i + 1 < len(lines) and re.match(r'^\s+disabled:\s*true\b', lines[i + 1]):
                pass
            else:
                # Escape reason for YAML double-quoted scalar
                r = reason.replace('\\', '\\\\').replace('"', "'")
                out.append('  disabled: true')
                out.append(f'  disabled_reason: "{r}"')
                out.append(f'  disabled_at: "{today}"')
                out.append('  disabled_by: "107-R2-spec-scan"')
                edited = True
        i += 1
    if edited:
        req_path.write_text("\n".join(out))
    return edited


def main():
    today = date.today().isoformat()
    total_scanned = 0
    total_disabled_now = 0
    total_already = 0
    by_reason = {}
    examples_by_reason = {}

    for req in CATEGORIES.glob("*/requirements.yaml"):
        text = req.read_text(errors="replace")
        # Walk entries by id boundaries (tolerant — works even on yaml-broken files)
        entries = re.split(r"(?m)^(?=- id: )", text)
        for entry in entries:
            m = re.match(r'- id:\s*["\']?([A-Z]+-\d+)["\']?', entry)
            if not m:
                continue
            pid = m.group(1)
            total_scanned += 1
            # Pull description + output_format + title from this entry
            desc_match = re.search(r'\bdescription:\s*(.+?)$', entry, re.MULTILINE)
            of_match = re.search(r'\boutput_format:\s*(.+?)$', entry, re.MULTILINE)
            title_match = re.search(r'\btitle:\s*(.+?)$', entry, re.MULTILINE)
            blob = " ".join(filter(None, [
                (desc_match.group(1) if desc_match else ""),
                (of_match.group(1) if of_match else ""),
                (title_match.group(1) if title_match else ""),
            ]))
            reason = classify_spec(blob)
            if not reason:
                continue
            # Already disabled?
            if re.search(r'^\s+disabled:\s*true\b', entry, re.MULTILINE):
                total_already += 1
                continue
            short_reason = f"[{reason}] auto-flagged from spec scan: {blob[:140].strip()}"
            if disable_in_file(req, pid, short_reason, today):
                total_disabled_now += 1
                by_reason[reason] = by_reason.get(reason, 0) + 1
                examples_by_reason.setdefault(reason, []).append(pid)

    print(f"Scanned {total_scanned} programs")
    print(f"Already disabled (skipped): {total_already}")
    print(f"Newly disabled by spec scan: {total_disabled_now}")
    print()
    for r in sorted(by_reason, key=lambda x: -by_reason[x]):
        ex = ", ".join(examples_by_reason[r][:8])
        more = f" (+ {len(examples_by_reason[r]) - 8} more)" if len(examples_by_reason[r]) > 8 else ""
        print(f"  {r}: {by_reason[r]}")
        print(f"    examples: {ex}{more}")


if __name__ == "__main__":
    main()
