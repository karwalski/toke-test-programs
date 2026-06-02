#!/usr/bin/env python3
"""Token comparison framework: toke vs Python programs.

Compares byte sizes (and later, BPE token counts) between toke and Python
solutions for all programs that have both.
"""

import json
import os
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOLUTIONS_DIR = ROOT / "results" / "solutions"
PYTHON_REFS_DIR = ROOT / "results" / "python-refs"
OUTPUT_FILE = ROOT / "results" / "token-comparison.json"


def find_pairs():
    """Find all programs that have both a toke and Python solution."""
    pairs = []
    if not SOLUTIONS_DIR.is_dir() or not PYTHON_REFS_DIR.is_dir():
        return pairs

    for category_dir in sorted(SOLUTIONS_DIR.iterdir()):
        if not category_dir.is_dir():
            continue
        category = category_dir.name
        for id_dir in sorted(category_dir.iterdir()):
            if not id_dir.is_dir():
                continue
            prog_id = id_dir.name
            toke_file = id_dir / "solution.tk"
            python_file = PYTHON_REFS_DIR / category / prog_id / "solution.py"
            if toke_file.is_file() and python_file.is_file():
                pairs.append({
                    "id": prog_id,
                    "category": category,
                    "toke_path": toke_file,
                    "python_path": python_file,
                })
    return pairs


def count_bytes(path):
    """Return file size in bytes."""
    return path.stat().st_size


def build_report(pairs):
    """Build the full comparison report."""
    programs = []
    for p in pairs:
        toke_bytes = count_bytes(p["toke_path"])
        python_bytes = count_bytes(p["python_path"])
        byte_ratio = python_bytes / toke_bytes if toke_bytes > 0 else None
        programs.append({
            "id": p["id"],
            "category": p["category"],
            "toke_bytes": toke_bytes,
            "python_bytes": python_bytes,
            "byte_ratio": round(byte_ratio, 4) if byte_ratio is not None else None,
            "toke_bpe_tokens": None,
            "python_cl100k_tokens": None,
            "token_ratio": None,
        })

    # Summary
    toke_bytes_list = [p["toke_bytes"] for p in programs]
    python_bytes_list = [p["python_bytes"] for p in programs]
    ratios = [p["byte_ratio"] for p in programs if p["byte_ratio"] is not None]

    summary = {
        "avg_toke_bytes": round(statistics.mean(toke_bytes_list), 2) if toke_bytes_list else 0,
        "avg_python_bytes": round(statistics.mean(python_bytes_list), 2) if python_bytes_list else 0,
        "avg_byte_ratio": round(statistics.mean(ratios), 4) if ratios else 0,
        "median_byte_ratio": round(statistics.median(ratios), 4) if ratios else 0,
    }

    # By category
    by_category = {}
    cat_groups = {}
    for p in programs:
        cat_groups.setdefault(p["category"], []).append(p)
    for cat in sorted(cat_groups):
        items = cat_groups[cat]
        cat_ratios = [i["byte_ratio"] for i in items if i["byte_ratio"] is not None]
        by_category[cat] = {
            "count": len(items),
            "avg_toke_bytes": round(statistics.mean([i["toke_bytes"] for i in items]), 2),
            "avg_python_bytes": round(statistics.mean([i["python_bytes"] for i in items]), 2),
            "avg_ratio": round(statistics.mean(cat_ratios), 4) if cat_ratios else 0,
        }

    report = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "total_pairs": len(programs),
        "summary": summary,
        "by_category": by_category,
        "programs": programs,
    }
    return report


def print_summary(report):
    """Print a human-readable summary to stdout."""
    s = report["summary"]
    n = report["total_pairs"]

    print("=" * 64)
    print("  Token Comparison: toke vs Python (byte-level)")
    print("=" * 64)
    print()
    print(f"  Total pairs found:       {n}")
    print(f"  Avg toke bytes:          {s['avg_toke_bytes']:.0f}")
    print(f"  Avg Python bytes:        {s['avg_python_bytes']:.0f}")
    print(f"  Avg byte ratio (Py/tk):  {s['avg_byte_ratio']:.4f}")
    print(f"  Median byte ratio:       {s['median_byte_ratio']:.4f}")
    print()

    # By category
    print("-" * 64)
    print(f"  {'Category':<28} {'Count':>5}  {'Avg tk':>8}  {'Avg Py':>8}  {'Ratio':>7}")
    print("-" * 64)
    for cat, data in sorted(report["by_category"].items()):
        print(f"  {cat:<28} {data['count']:>5}  {data['avg_toke_bytes']:>8.0f}  {data['avg_python_bytes']:>8.0f}  {data['avg_ratio']:>7.4f}")
    print()

    # Top 10 most compact (highest ratio = Python much bigger)
    ranked = sorted(
        [p for p in report["programs"] if p["byte_ratio"] is not None],
        key=lambda p: p["byte_ratio"],
        reverse=True,
    )

    print("-" * 64)
    print("  Top 10: toke MOST compact vs Python (highest Py/tk ratio)")
    print("-" * 64)
    print(f"  {'ID':<12} {'Category':<28} {'tk':>6} {'Py':>6} {'Ratio':>7}")
    for p in ranked[:10]:
        print(f"  {p['id']:<12} {p['category']:<28} {p['toke_bytes']:>6} {p['python_bytes']:>6} {p['byte_ratio']:>7.2f}")
    print()

    print("-" * 64)
    print("  Top 10: toke LEAST compact vs Python (lowest Py/tk ratio)")
    print("-" * 64)
    print(f"  {'ID':<12} {'Category':<28} {'tk':>6} {'Py':>6} {'Ratio':>7}")
    for p in ranked[-10:]:
        print(f"  {p['id']:<12} {p['category']:<28} {p['toke_bytes']:>6} {p['python_bytes']:>6} {p['byte_ratio']:>7.2f}")
    print()

    print(f"  Report written to: {OUTPUT_FILE}")
    print()


def main():
    pairs = find_pairs()
    if not pairs:
        print("No matching toke/Python pairs found.", file=sys.stderr)
        sys.exit(1)

    report = build_report(pairs)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(report, f, indent=2)

    print_summary(report)


if __name__ == "__main__":
    main()
