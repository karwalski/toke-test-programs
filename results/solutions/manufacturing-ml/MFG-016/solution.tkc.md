# Investment Yield Calculator - Documentation

**File:** `rolledyield.tkc.md`

## Overview

This program calculates a rolled yield by reading CSV-formatted data from standard input and multiplying successive yield values. It outputs the final result as a JSON object with the rolled yield rounded to two decimal places.

## Architecture

**Single Module Design:**
- **Module:** `rolledyield`
- **Main Function:** `main()` - Core processing loop with input parsing and yield calculation
- **Dependencies:** Standard I/O (`std.io`) and string manipulation (`std.str`)
- **Data Flow:** stdin → CSV parsing → yield multiplication → JSON output → stdout

## Key Concepts

**Toke Language Features Demonstrated:**
- **Mutable Variables:** `mut` keyword for `yield` and `count` state tracking
- **Standard Library Usage:** Extensive use of `std.io` and `std.str` modules
- **Loop Control:** `lp(true)` infinite loop with `br` break condition
- **Type System:** Implicit type handling with float conversions
- **String Operations:** Splitting, concatenation, and format conversion

## Line-by-Line Notes

```toke
m=rolledyield;i=io:std.io;i=s:std.str;
```
Module declaration and library imports with aliases for conciseness.

```toke
let yield=mut.1.0;let count=mut.0;
```
Initialize mutable yield accumulator to 1.0 and line counter to 0.

```toke
if(count>1){let parts=s.split(line;",");if(parts.len()>=2){...}}
```
Skip first line (likely header) and ensure valid CSV format with at least 2 columns.

```toke
let v=s.tofloat(parts.get(1));yield=yield*v
```
Extract second column value, convert to float, and multiply into running yield.

```toke
let r=s.tofloat(s.format(yield;"%.2f"));
```
Round final yield to 2 decimal places using format-then-parse technique.

```toke
io.println(s.concat(s.concat("{\"rty\":";s.fromfloat(r));"}"));
```
Construct and output JSON response with nested string concatenations.

## Test Coverage

**Recommended Test Cases:**
- **Empty Input:** Verify graceful handling of no data lines
- **Single Data Row:** Confirm yield remains 1.0 when only header exists
- **Multiple Valid Rows:** Test multiplicative accumulation (e.g., 1.5 × 0.8 = 1.2)
- **Malformed CSV:** Ensure robustness with missing commas or columns
- **Edge Values:** Test with zero, negative, and very large yield values
- **Precision:** Verify 2-decimal rounding accuracy

## Complexity

**Time Complexity:** O(n) where n is the number of input lines
**Space Complexity:** O(1) - constant memory usage regardless of input size
**I/O Bound:** Performance primarily limited by stdin read operations

## Potential Improvements

1. **Error Handling:** Add validation for non-numeric yield values and graceful error messages
2. **Configuration:** Make column index configurable rather than hardcoded to index 1
3. **Output Format:** Support multiple output formats (plain text, XML) beyond JSON
4. **Code Structure:** Extract CSV parsing and JSON formatting into separate functions
5. **Memory Efficiency:** Consider streaming approach for extremely large datasets
6. **Validation:** Add bounds checking for reasonable yield value ranges
7. **Documentation:** Include inline comments for better maintainability

**Security Considerations:** Input sanitization for production use with untrusted CSV data.