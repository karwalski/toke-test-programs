# csvfromjson.tkc.md

## Overview

This Toke program converts JSON data to CSV format by parsing JSON objects and extracting key-value pairs into comma-separated values. The program reads JSON input from standard input, processes it character by character to build CSV headers and rows, then outputs the formatted CSV data.

## Architecture

The program consists of:
- **Module imports**: Standard I/O and string manipulation libraries
- **Helper function**: `isalnum()` for character validation (currently only checks digits 0-9)
- **Main parsing engine**: Character-by-character JSON parser with state machine logic
- **Output generation**: CSV formatting with proper quoting for values containing spaces

Data flows from stdin → JSON parser → CSV formatter → stdout.

## Key Concepts

**Toke Language Features Demonstrated:**
- Module importing (`std.io`, `std.str`)
- Function definitions with type annotations (`$str`, `$bool`, `$i64`)
- Mutable variables (`mut.""`, `mut.0`)
- String manipulation and concatenation
- Control flow with `if/el` and `lp` (loop) constructs
- Early returns with `<` operator

## Line-by-Line Notes

**Lines 1-3**: Module imports and aliases for CSV conversion, I/O, and string operations

**Lines 4**: `isalnum()` function - incomplete implementation that only checks for digits 0-9, not full alphanumeric characters

**Lines 6-15**: Variable initialization using mutable references for parsing state:
- `instr`: tracks if parser is inside a quoted string
- `isval`: indicates if currently parsing a value (vs. key)
- `objcount`/`keycount`: track object and key positions
- `curisstr`: flags if current value was originally a string

**Lines 17-19**: Quote handling - toggles string state and marks values that were quoted

**Lines 21-25**: Object start (`{`) - resets parsing state

**Lines 26-31**: Colon (`:`) handling - builds CSV headers from first object's keys

**Lines 32-42**: Comma (`,`) handling - processes values and builds CSV rows with conditional quoting

**Lines 43-54**: Object end (`}`) handling - completes rows and increments object counter

**Lines 55-56**: Value character accumulation during parsing

## Test Coverage

The program lacks explicit test cases. Recommended test scenarios:
- Simple JSON objects with string/numeric values
- JSON with nested structures (may fail)
- Values containing spaces (tests quoting logic)
- Multiple objects in array format
- Edge cases: empty objects, special characters, escaped quotes

## Complexity

**Time Complexity**: O(n) where n is the input JSON string length
**Space Complexity**: O(m) where m is the size of the output CSV

The character-by-character parsing approach is efficient for streaming but builds result strings incrementally.

## Potential Improvements

1. **Complete `isalnum()` function**: Add support for letters A-Z, a-z
2. **Robust JSON parsing**: Handle escaped characters, nested objects, arrays
3. **Error handling**: Validate JSON syntax and provide meaningful error messages  
4. **Memory optimization**: Use string builders instead of repeated concatenation
5. **Flexible input**: Support JSON arrays of objects, not just individual objects
6. **CSV escaping**: Proper handling of quotes, commas, and newlines in values
7. **Type preservation**: Better handling of numeric vs. string values in output
8. **Code organization**: Break parsing logic into smaller, testable functions