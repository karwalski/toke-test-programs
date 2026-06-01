# audit.tkc.md

## Overview

This Toke program analyzes software project dependencies for license compatibility issues. It reads project information and dependency data in JSON format, then identifies packages with copyleft licenses (GPL variants) that may be incompatible with the target project's licensing requirements.

## Architecture

The program is structured around three main functions:
- **`copyleft()`** — License classification utility that detects GPL-family licenses
- **`extract()`** — JSON parsing helper that extracts quoted string values by key
- **`main()`** — Primary control flow that processes input and generates compatibility reports

**Data Flow:**
1. Read project name and JSON dependency data from stdin
2. Split JSON into object segments using `}` delimiter
3. For each segment containing "package", extract package name and license
4. Classify license compatibility and output formatted results

## Key Concepts

**Toke Language Features Demonstrated:**
- **Module imports** — Uses `std.io` and `std.str` standard library modules
- **Type annotations** — Explicit parameter and return types (`$str`, `$bool`, `$i64`)
- **String manipulation** — Heavy use of `split()`, `contains()`, `concat()`, `trim()`
- **Control structures** — `if/el` conditionals and `lp` (loop) constructs
- **Early returns** — Uses `<value` syntax for function returns
- **Variable binding** — `let` declarations with lexical scoping

## Line-by-Line Notes

**Lines 1-2:** Module imports using alias syntax (`i=io:std.io`)

**Lines 3-4:** `copyleft()` function checks for both "GPL" and "gpl" variants, demonstrating case-sensitive string matching requirements

**Lines 5-9:** `extract()` implements basic JSON value extraction by:
- Splitting on the key to find the field
- Re-splitting on quotes to isolate the value
- Using array bounds checking (`len()>=2`) for safety

**Lines 15-16:** Nested `extract()` calls parse package name and license from each JSON object segment

**Lines 17-19:** Complex string concatenation builds formatted output messages with conditional logic for compatibility status

## Test Coverage

The program should be tested with:
- **Positive cases:** JSON containing GPL, LGPL, AGPL licensed packages
- **Negative cases:** MIT, BSD, Apache licensed packages  
- **Edge cases:** Malformed JSON, missing license fields, case variations
- **Boundary conditions:** Empty input, single package, large dependency lists

## Complexity

**Time Complexity:** O(n*m) where n = number of JSON objects and m = average string length for splitting/searching operations

**Space Complexity:** O(k) where k = size of largest JSON object segment stored in memory

## Potential Improvements

1. **Robust JSON Parsing** — Replace string splitting with proper JSON parser for better reliability
2. **License Detection** — Expand copyleft detection to include LGPL, AGPL, and other variants
3. **Error Handling** — Add validation for malformed input and graceful failure modes
4. **Configuration** — Allow customizable license compatibility rules via external config
5. **Output Formatting** — Support multiple output formats (JSON, CSV, structured reports)
6. **Performance** — Optimize string operations for large dependency lists
7. **Case Handling** — Normalize license strings to handle mixed case consistently