#!/usr/bin/env python3
"""Validate uniqueness and diversity of toke test program requirements.

Loads all requirements.yaml files from categories/*, checks for duplicates,
similar titles/descriptions, and diversity of stdlib modules, difficulty
levels, and I/O patterns.

Exit code 0 if all checks pass, 1 if issues found.
"""

import os
import sys
import yaml
from pathlib import Path
from itertools import combinations


def jaccard_similarity(text_a: str, text_b: str) -> float:
    """Compute Jaccard similarity between two texts based on word sets."""
    words_a = set(text_a.lower().split())
    words_b = set(text_b.lower().split())
    if not words_a or not words_b:
        return 0.0
    intersection = words_a & words_b
    union = words_a | words_b
    return len(intersection) / len(union)


def word_overlap_ratio(text_a: str, text_b: str) -> float:
    """Compute word overlap as intersection / min set size (>80% check)."""
    words_a = set(text_a.lower().split())
    words_b = set(text_b.lower().split())
    if not words_a or not words_b:
        return 0.0
    intersection = words_a & words_b
    min_size = min(len(words_a), len(words_b))
    return len(intersection) / min_size


def load_all_requirements(base_dir: Path) -> dict:
    """Load all requirements.yaml files, keyed by category name."""
    categories_dir = base_dir / "categories"
    all_reqs = {}

    for category_dir in sorted(categories_dir.iterdir()):
        if not category_dir.is_dir():
            continue
        req_file = category_dir / "requirements.yaml"
        if not req_file.exists():
            continue
        with open(req_file, "r") as f:
            data = yaml.safe_load(f)
        if data and "requirements" in data:
            all_reqs[category_dir.name] = data["requirements"]
        elif isinstance(data, list):
            all_reqs[category_dir.name] = data

    return all_reqs


def check_duplicate_ids(all_reqs: dict) -> list:
    """Check for duplicate IDs across all categories."""
    seen_ids = {}
    duplicates = []

    for category, reqs in all_reqs.items():
        for req in reqs:
            req_id = req.get("id", "")
            if not req_id:
                continue
            if req_id in seen_ids:
                duplicates.append(
                    f"Duplicate ID '{req_id}' in '{category}' "
                    f"(first seen in '{seen_ids[req_id]}')"
                )
            else:
                seen_ids[req_id] = category

    return duplicates


def check_similar_titles(all_reqs: dict, threshold: float = 0.80) -> list:
    """Check for similar titles (>80% word overlap)."""
    flagged = []
    all_items = []

    for category, reqs in all_reqs.items():
        for req in reqs:
            title = req.get("title", "")
            req_id = req.get("id", "unknown")
            if title:
                all_items.append((req_id, category, title))

    for (id_a, cat_a, title_a), (id_b, cat_b, title_b) in combinations(all_items, 2):
        overlap = word_overlap_ratio(title_a, title_b)
        if overlap > threshold:
            flagged.append(
                f"Similar titles ({overlap:.0%}): "
                f"'{id_a}' ({cat_a}): \"{title_a}\" vs "
                f"'{id_b}' ({cat_b}): \"{title_b}\""
            )

    return flagged


def check_similar_descriptions(all_reqs: dict, threshold: float = 0.70) -> list:
    """Check for similar descriptions (>70% Jaccard similarity)."""
    flagged = []
    all_items = []

    for category, reqs in all_reqs.items():
        for req in reqs:
            desc = req.get("description", "")
            req_id = req.get("id", "unknown")
            if desc:
                all_items.append((req_id, category, desc))

    for (id_a, cat_a, desc_a), (id_b, cat_b, desc_b) in combinations(all_items, 2):
        similarity = jaccard_similarity(desc_a, desc_b)
        if similarity > threshold:
            flagged.append(
                f"Similar descriptions (Jaccard {similarity:.0%}): "
                f"'{id_a}' ({cat_a}) vs '{id_b}' ({cat_b})"
            )

    return flagged


def check_diversity(all_reqs: dict) -> list:
    """Check diversity within each category."""
    warnings = []

    for category, reqs in all_reqs.items():
        total = len(reqs)
        if total == 0:
            continue

        # Check stdlib module diversity (no more than 50% using same module)
        module_counts = {}
        for req in reqs:
            modules = req.get("stdlib_modules", [])
            if isinstance(modules, str):
                modules = [modules]
            for mod in (modules or []):
                module_counts[mod] = module_counts.get(mod, 0) + 1

        for mod, count in module_counts.items():
            if count / total > 0.50:
                warnings.append(
                    f"[{category}] Module '{mod}' used by {count}/{total} "
                    f"requirements ({count/total:.0%} > 50% limit)"
                )

        # Check difficulty level diversity
        difficulty_counts = {}
        for req in reqs:
            level = req.get("difficulty", None)
            if level is not None:
                difficulty_counts[level] = difficulty_counts.get(level, 0) + 1

        # All levels 1-5 should be represented
        for level in range(1, 6):
            if level not in difficulty_counts:
                warnings.append(
                    f"[{category}] Difficulty level {level} not represented"
                )

        # No more than 40% at any single level
        for level, count in difficulty_counts.items():
            if count / total > 0.40:
                warnings.append(
                    f"[{category}] Difficulty {level} has {count}/{total} "
                    f"requirements ({count/total:.0%} > 40% limit)"
                )

        # Check I/O pattern diversity
        io_counts = {}
        for req in reqs:
            io_pattern = req.get("io_pattern", req.get("io_type", "unknown"))
            if io_pattern:
                io_counts[io_pattern] = io_counts.get(io_pattern, 0) + 1

        expected_io = {"line-based", "json", "csv", "multi-line"}
        found_io = set(io_counts.keys())
        missing_io = expected_io - found_io
        if missing_io and len(found_io) > 0:
            warnings.append(
                f"[{category}] Missing I/O patterns: {', '.join(sorted(missing_io))}"
            )

    return warnings


def main():
    base_dir = Path(__file__).resolve().parent.parent
    all_reqs = load_all_requirements(base_dir)

    issues_found = False

    # Summary counts
    print("=" * 60)
    print("UNIQUENESS AND DIVERSITY VALIDATION REPORT")
    print("=" * 60)
    print()

    # Total requirements per category
    print("Requirements per category:")
    grand_total = 0
    coverage_gaps = []
    for category in sorted(all_reqs.keys()):
        count = len(all_reqs[category])
        grand_total += count
        status = ""
        if count < 125:
            status = f"  [COVERAGE GAP: needs {125 - count} more]"
            coverage_gaps.append((category, count))
        print(f"  {category}: {count}{status}")

    print(f"\n  Grand total: {grand_total}")
    print()

    # Duplicate IDs
    print("-" * 60)
    print("DUPLICATE IDS:")
    duplicates = check_duplicate_ids(all_reqs)
    if duplicates:
        issues_found = True
        for d in duplicates:
            print(f"  ERROR: {d}")
    else:
        print("  None found.")
    print()

    # Similar titles
    print("-" * 60)
    print("SIMILAR TITLES (>80% word overlap):")
    similar_titles = check_similar_titles(all_reqs)
    if similar_titles:
        issues_found = True
        for s in similar_titles:
            print(f"  WARNING: {s}")
    else:
        print("  None found.")
    print()

    # Similar descriptions
    print("-" * 60)
    print("SIMILAR DESCRIPTIONS (>70% Jaccard similarity):")
    similar_descs = check_similar_descriptions(all_reqs)
    if similar_descs:
        issues_found = True
        for s in similar_descs:
            print(f"  WARNING: {s}")
    else:
        print("  None found.")
    print()

    # Diversity warnings
    print("-" * 60)
    print("DIVERSITY WARNINGS:")
    diversity_warnings = check_diversity(all_reqs)
    if diversity_warnings:
        issues_found = True
        for w in diversity_warnings:
            print(f"  WARNING: {w}")
    else:
        print("  All diversity checks passed.")
    print()

    # Coverage gaps
    print("-" * 60)
    print("COVERAGE GAPS (categories with <125 requirements):")
    if coverage_gaps:
        issues_found = True
        for category, count in coverage_gaps:
            print(f"  WARNING: {category} has only {count}/125 requirements")
    else:
        print("  All categories meet minimum requirement count.")
    print()

    print("=" * 60)
    if issues_found:
        print("RESULT: ISSUES FOUND - review warnings above")
        sys.exit(1)
    else:
        print("RESULT: ALL CHECKS PASSED")
        sys.exit(0)


if __name__ == "__main__":
    main()
