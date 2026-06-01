# streak.tkc.md

## Overview

This Toke program analyzes a sequence of date strings to calculate daily streak statistics. It reads dates from standard input, parses them into a comparable format, and computes both the current streak length and the longest streak of consecutive days.

## Architecture

The program consists of two main functions:

- **`parsedate()`** — Date parsing utility that converts "YYYY-MM-DD" strings to integer format
- **`main()`** — Primary logic handler that reads input, processes dates, and calculates streaks

Data flows from stdin through string parsing, array accumulation, sequential analysis, and finally to formatted output.

## Key Concepts

- **String manipulation** — Uses `std.str` for splitting, trimming, and conversion operations
- **Mutable variables** — Demonstrates `mut.` syntax for loop counters and accumulator variables
- **Dynamic arrays** — Shows array construction with `mut.@()` and element access patterns
- **Control flow** — Nested conditionals with `if/el` and loop control with `lp/br`
- **Type annotations** — Function signatures specify `$str`, `$i64` parameter and return types

## Line-by-Line Notes

**Date parsing logic:**
- `<year*10000+month*100+day>` creates sortable integer representation (e.g., "2024-03-15" → 20240315)
- Returns `<0` for malformed dates as error sentinel

**Input processing:**
- `lp(1){...}` creates infinite loop, broken by empty line detection
- `s.trim(io.readln())` handles whitespace around input dates

**Streak calculation:**
- `curr=prev+1` checks for consecutive day integers (works due to YYYYMMDD format)
- Tracks both running streak and maximum encountered streak
- Handles edge case where final streak might be the longest

## Test Coverage

Ideal test cases should verify:
- **Valid date sequences** — Consecutive and non-consecutive date patterns
- **Edge cases** — Single date, empty input, malformed date strings
- **Streak boundaries** — Multiple streaks of varying lengths
- **Input formats** — Whitespace handling and termination conditions

## Complexity

- **Time:** O(n) where n is number of input dates
- **Space:** O(n) for storing parsed dates array

The algorithm makes two linear passes: one for input collection, one for streak analysis.

## Potential Improvements

1. **Memory optimization** — Stream processing could eliminate date storage array
2. **Date validation** — Add bounds checking for month/day ranges and leap years
3. **Error handling** — Explicit error messages for invalid date formats
4. **Input flexibility** — Support multiple date formats beyond YYYY-MM-DD
5. **Output formatting** — Add options for different report styles or JSON output
6. **Performance** — Consider in-place streak calculation during input parsing