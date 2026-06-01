# Content Moderation System - Documentation

**File:** `violation.tkc.md`

## Overview

This Toke program implements a basic content moderation system that analyzes JSON input containing text messages and flags potentially harmful content. The system scans for predefined violation patterns (harassment and threats) and outputs a structured JSON report indicating whether content should be flagged and what specific violations were detected.

## Architecture

The program follows a linear processing pipeline within a single `main()` function:

1. **Input Processing** — Reads JSON input and extracts the text field using string manipulation
2. **Pattern Matching** — Checks extracted text against hardcoded violation patterns
3. **Violation Tracking** — Builds an array of violation objects for flagged content
4. **Output Generation** — Constructs and outputs a JSON response with flagging results

**Module Dependencies:**
- `std.io` — Input/output operations
- `std.str` — String manipulation and searching
- `violation` (main module) — Core moderation logic

## Key Concepts

**Toke Language Features Demonstrated:**
- **Module imports** with aliasing (`i=io:std.io`, `i=s:std.str`)
- **Mutable variables** (`mut.@()`, `mut.false`, `mut.0`)
- **Array operations** with `@()` constructor and `.get()` access
- **String manipulation** using stdlib functions (`indexof`, `slice`, `contains`, `concat`)
- **Conditional logic** with `if`/`el` (else) branching
- **Loop constructs** using `lp()` for iteration
- **Type annotations** (`$i64` return type)

## Line-by-Line Notes

**JSON Parsing (Lines 1-4):**
```toke
let idxtext=s.indexof(input;"\"text\":\"")
let start=idxtext+8
```
Manual JSON parsing by finding the `"text":"` pattern and calculating the content start position (+8 accounts for the pattern length).

**Violation Detection (Lines 6-7):**
```toke
if(s.contains(text;"idiot")){flagged=true;...}
```
Simple substring matching for violation patterns. Each violation type has hardcoded severity levels and span text.

**Array Building Logic:**
```toke
if(violations.len=0){violations=@(...)}el{let temp=@(violations.get(0);...);violations=temp}
```
Demonstrates immutable array reconstruction pattern since Toke arrays appear to be immutable by default.

**JSON Output Construction:**
```toke
lp(idx<violations.len){if(idx>0){result=s.concat(result;",")};...}
```
Manual JSON serialization with comma separation handling for array elements.

## Test Coverage

To properly test this system, verify:

1. **Valid JSON input** with text field extraction
2. **Harassment detection** with "idiot" keyword
3. **Threat detection** with "find where you live" phrase  
4. **Multiple violations** in single input
5. **Clean content** producing unflagged output
6. **Edge cases** like empty text or malformed JSON

## Complexity

- **Time Complexity:** O(n×m) where n = input length, m = number of violation patterns
- **Space Complexity:** O(k) where k = number of detected violations
- **Scalability Limitations:** Linear scan approach doesn't scale well with large violation dictionaries

## Potential Improvements

1. **Robust JSON Parsing** — Replace manual string manipulation with proper JSON parser
2. **Configuration-Driven Rules** — Move violation patterns to external configuration files
3. **Pattern Matching Enhancement** — Implement regex support for more sophisticated detection
4. **Performance Optimization** — Use more efficient string searching algorithms (e.g., Aho-Corasick)
5. **Error Handling** — Add validation for malformed input and graceful failure modes
6. **Modularization** — Split into separate functions for parsing, detection, and output formatting
7. **Extensibility** — Design plugin architecture for custom violation detectors
8. **Case Sensitivity** — Add case-insensitive matching options
9. **Severity Scoring** — Implement weighted scoring system for multiple violations
10. **Logging** — Add audit trail for moderation decisions