# spcrules.tkc.md

## Overview

This Toke program implements a Statistical Process Control (SPC) rule checker that analyzes a comma-separated sequence of numeric data points. It specifically detects "7 points trending" violations, where 7 consecutive data points show a monotonic trend (either all increasing or all decreasing), and outputs the results in JSON format.

## Architecture

The program follows a linear, procedural structure:

- **Input Module**: Uses `std.io` for reading input and `std.str` for string processing
- **Data Processing**: Parses CSV input into individual numeric values
- **Trend Detection Engine**: Sliding window algorithm to check 7-point sequences
- **Output Module**: JSON formatter for rule violation reporting

The data flows from stdin → parsing → trend analysis → JSON output to stdout.

## Key Concepts

**Toke Language Features Demonstrated:**
- **Module imports**: `std.io` and `std.str` standard library usage
- **Mutable variables**: `mut` keyword for stateful computation
- **Type system**: Explicit `$i64` return type annotation
- **String manipulation**: `trim()`, `split()`, `concat()`, type conversions
- **Control flow**: `if/el` conditionals and `lp` (loop) constructs
- **Array operations**: `len()`, `get()` for indexed access

## Line-by-Line Notes

```toke
m=spcrules;i=io:std.io;i=s:std.str;
```
Module declaration and namespace aliases for I/O and string utilities.

```toke
let n=parts.len();let startidx=mut.0;let foundtrend=mut.false;
```
Track data length and maintain state for first trend detection (reports only the first violation found).

```toke
if(n>=7){let i=mut.0;lp(i<=n-7){
```
Sliding window bounds check: ensures at least 7 points exist, then iterates through valid starting positions.

```toke
let increasing=mut.true;let decreasing=mut.true;
```
Boolean flags reset for each window; both start true and get eliminated based on data relationships.

```toke
if(foundtrend=false){foundtrend=true;startidx=i}
```
First-violation-only logic: captures the earliest trend occurrence and ignores subsequent ones.

## Test Coverage

**Essential Test Cases:**
- **Positive Cases**: 7+ increasing values, 7+ decreasing values, mixed data with embedded trends
- **Boundary Cases**: Exactly 7 points, fewer than 7 points, single/empty input
- **Edge Cases**: Equal consecutive values (should not trigger), multiple trends (only first reported)
- **Data Validation**: Non-numeric input handling, whitespace variations, malformed CSV

## Complexity

- **Time Complexity**: O(n²) where n is the number of data points
  - Outer loop: O(n) iterations
  - Inner loop: O(6) = O(1) for each window comparison
  - Overall: O(n × 6) = O(n) per window × O(n) windows = O(n²)
- **Space Complexity**: O(n) for storing the split string array

## Potential Improvements

1. **Performance Optimization**: Reduce to O(n) by tracking trend state across sliding window movements instead of recalculating each window independently

2. **Multiple Rule Detection**: Extend architecture to support additional SPC rules (runs, shifts, cycles) with a plugin-based checker system

3. **Enhanced Output**: Include trend direction, affected data values, and confidence metrics in JSON response

4. **Input Validation**: Add explicit error handling for malformed numeric data and provide meaningful error messages

5. **Configuration**: Make trend length (currently hardcoded to 7) and detection sensitivity configurable parameters

6. **Streaming Support**: Process large datasets incrementally rather than loading entire input into memory