# gradecheck.tkc.md

## Overview

This program analyzes text readability by calculating a reading grade level based on average word length. It compares the calculated grade level against a target grade and outputs whether the text is appropriate, too easy, or too hard for the intended audience.

## Architecture

The program is structured as a single module (`gradecheck`) with four main functions:

- **`wordcount(text)`** — Counts words in input text by splitting on spaces and filtering empty strings
- **`avgwordlen(text)`** — Calculates average word length across all words in the text
- **`gradelevel(text)`** — Maps average word length to educational grade levels using a simple heuristic
- **`main()`** — Orchestrates input/output and grade comparison logic

**Data Flow:**
1. Read target grade and text from stdin
2. Calculate actual grade level using word length analysis
3. Compare and output appropriateness assessment

## Key Concepts

- **Module System**: Uses `std.io` and `std.str` standard library modules with aliasing (`i=io`, `i=s`)
- **Type System**: Explicit type annotations (`$str`, `$i64`) for function parameters and returns
- **Mutable Variables**: `mut` keyword for counters and accumulators
- **Control Flow**: `lp` (loop) constructs and nested `if-el` conditionals
- **String Operations**: Extensive use of `split`, `trim`, `concat`, and conversion functions

## Line-by-Line Notes

**Module Declaration & Imports:**
- `m=gradecheck` — Module name declaration
- Import aliases reduce verbosity in function calls

**wordcount() Function:**
- Uses manual loop with mutable index rather than iterator pattern
- `s.trim()` handles potential whitespace around words after splitting
- Filters empty strings to avoid counting multiple consecutive spaces

**avgwordlen() Function:**
- Tracks both total character length and word count separately
- Division-by-zero protection returns 0 for empty text
- Integer division truncates decimal portions

**gradelevel() Function:**
- Implements a simple readability heuristic mapping average word length to grade levels
- Grade mapping: ≤3 chars→Grade 1, ≤4→Grade 2, ≤5→Grade 5, ≤6→Grade 8, ≤7→Grade 10, >7→Grade 14
- Uses nested `if-el` chain rather than switch/case construct

**main() Function:**
- String concatenation pattern builds output messages dynamically
- Three-way comparison determines text difficulty relative to target

## Test Coverage

To thoroughly test this program, verify:
- **Edge Cases**: Empty text, single word, text with multiple spaces
- **Grade Boundaries**: Text with average word lengths at each threshold (3, 4, 5, 6, 7+ characters)
- **Comparison Logic**: Inputs where calculated grade is below, equal to, and above target grade
- **Input Validation**: Non-numeric target grades, empty input lines

## Complexity

- **Time Complexity**: O(n) where n is the total number of characters in input text
- **Space Complexity**: O(w) where w is the number of words (due to `split()` creating word array)
- Both `wordcount()` and `avgwordlen()` perform similar O(n) passes over the split word array

## Potential Improvements

1. **Readability Algorithm**: Replace simplistic word-length heuristic with established formulas (Flesch-Kincaid, Gunning Fog)
2. **Sentence Analysis**: Incorporate sentence length and complexity for more accurate grade assessment
3. **Error Handling**: Add validation for non-numeric target grade input and graceful failure modes
4. **Performance**: Combine `wordcount()` and `avgwordlen()` into single pass to avoid duplicate string processing
5. **Output Formatting**: More descriptive feedback including actual metrics (word count, average length, etc.)
6. **Code Style**: Extract magic numbers (grade thresholds) into named constants for maintainability