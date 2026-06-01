# Submission Analyzer - Companion Documentation (.tkc.md)

## Overview

This Toke program analyzes student submission data by parsing JSON-like input containing due dates, total students, and submission dates. It calculates and reports the percentage of submissions that were on-time, late, or missing, providing a statistical breakdown of assignment completion patterns.

## Architecture

The program consists of two main functions operating in a single-pass parser architecture:

- **`parsedate()`** — Utility function that converts date strings (YYYY-MM-DD format) into comparable integer representations
- **`main()`** — Core parsing engine that manually processes JSON-like input character by character, extracting key fields and computing statistics
- **Data Flow**: Raw input → Character-level parsing → Field extraction → Date comparison → Statistical calculation → Formatted output

## Key Concepts

**Toke Language Features Demonstrated:**
- **Module System**: Uses `std.io` and `std.str` standard library modules
- **Type System**: Explicit type annotations (`$str`, `$i64`) for function signatures
- **Mutable Variables**: `mut` keyword for variables that change during iteration
- **String Manipulation**: Extensive use of `slice()`, `split()`, `len()`, and string concatenation
- **Manual Memory Management**: Character-by-character parsing without built-in JSON support
- **Control Flow**: Nested loops (`lp`) and conditional branching for parsing logic

## Line-by-Line Notes

**Date Parsing (Lines 1-2):**
```toke
f=parsedate(datestr:$str):$i64{let parts=s.split(datestr;"-");
```
Converts "YYYY-MM-DD" format into integer (YYYYMMDD) for easy comparison.

**Main Parser Setup (Lines 3-4):**
```toke
let ontime=mut.0;let late=mut.0;let missing=mut.0;
```
Initializes counters as mutable variables for tracking submission categories.

**Character-Level JSON Parsing (Lines 5-6):**
```toke
lp(pos<len){let ch=s.slice(line;pos;pos+1);if(ch="\""){
```
Manual JSON parser that identifies quoted keys by scanning for quote characters.

**Field-Specific Parsing:**
- **due_date**: Extracts and converts due date for comparison baseline
- **total_students**: Parses total count for percentage calculations
- **submitted_date**: Compares against due date to categorize submission timing

**Statistical Output (Final lines):**
Uses string concatenation to format percentage reports with calculated ratios.

## Test Coverage

The program should be tested with:
- **Valid JSON**: Complete records with all required fields
- **Edge Cases**: Missing submissions, submissions exactly on due date
- **Date Formats**: Various date string formats and invalid dates
- **Boundary Conditions**: Zero students, 100% late submissions
- **Malformed Input**: Invalid JSON structure, missing quotes, incomplete records

## Complexity

**Time Complexity**: O(n) where n is the input string length
- Single-pass character scanning with constant-time operations per character

**Space Complexity**: O(1) 
- Fixed number of variables regardless of input size
- String slicing may create temporary substrings but overall space usage is constant

## Potential Improvements

1. **Error Handling**: Add validation for malformed JSON, invalid dates, and missing required fields
2. **JSON Library**: Replace manual parsing with proper JSON deserialization for robustness
3. **Input Flexibility**: Support multiple input formats beyond single-line JSON
4. **Performance**: Use proper date libraries instead of string-to-integer conversion
5. **Code Structure**: Extract parsing logic into separate functions for better modularity
6. **Output Format**: Add configurable output formats (CSV, JSON) and more detailed statistics
7. **Validation**: Check for logical consistency (e.g., submission dates before course start dates)
8. **Floating Point**: Use decimal arithmetic for more precise percentage calculations