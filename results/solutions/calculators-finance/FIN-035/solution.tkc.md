# weightconv.tkc.md

## Overview

This Toke program implements a weight conversion utility that converts between various weight units including kilograms, pounds, grams, ounces, and stones. The program reads user input as a space-separated command (amount, from-unit, to-unit) and outputs the converted weight value.

## Architecture

The program follows a functional architecture with three main layers:

- **Conversion Functions**: 12 pure conversion functions handling bidirectional conversions between unit pairs
- **Input Processing**: Command-line input parsing using string manipulation
- **Main Controller**: Nested conditional logic to route conversions based on source and target units

**Data Flow**: 
Input → Parse → Route to appropriate conversion function → Format output → Display

## Key Concepts

- **Type System**: Consistent use of `$f64` for floating-point calculations and `$i64` for return codes
- **Standard Library Usage**: 
  - `std.io` for input/output operations (`readln()`, `println()`)
  - `std.str` for string manipulation (`split()`, `tofloat()`, `fromfloat()`, `get()`)
- **Functional Programming**: Pure conversion functions with single expressions
- **Mutable Variables**: `mut.0.0` pattern for result accumulation
- **Module Declaration**: `m=weightconv` establishes module namespace

## Line-by-Line Notes

**Module & Imports**: `m=weightconv;i=io:std.io;i=s:std.str` - Module declaration with aliased standard library imports

**Conversion Functions**: Each follows pattern `f=name(param:$f64):$f64{<calculation}` where `<` indicates return value

**Main Function Structure**:
- `let parts=s.split(line;" ")` - Splits input on spaces for parsing
- `parts.len()>=3` - Validates minimum required arguments
- `s.tofloat(parts.get(0))` - Converts first argument to numeric amount
- Nested `if/el` chains route to appropriate conversion based on unit strings
- `result=mut.0.0` - Mutable result variable initialized to 0.0

**Error Handling**: Silent failure mode - invalid inputs result in 0.0 output

## Test Coverage

To verify this program, test cases should cover:

- **Valid Conversions**: Each supported unit pair (kg↔lb, g↔oz, etc.)
- **Precision**: Verify conversion factors (2.2046 for kg/lb, 35.274 for kg/oz, etc.)
- **Edge Cases**: Zero values, very large numbers, decimal precision
- **Invalid Input**: Missing arguments, invalid units, non-numeric amounts
- **Format Handling**: Extra whitespace, case sensitivity

## Complexity

- **Time Complexity**: O(1) - Constant time for any conversion
- **Space Complexity**: O(1) - Fixed memory usage regardless of input size
- **Input Processing**: O(n) where n is input string length (for splitting operation)

## Potential Improvements

1. **Error Handling**: Add explicit error messages for invalid inputs instead of silent failure
2. **Unit Validation**: Implement supported units list with validation
3. **Code Structure**: Replace nested conditionals with lookup table or match expressions
4. **Precision**: Use more precise conversion constants and handle floating-point rounding
5. **Extensibility**: Implement generic conversion framework for easy addition of new units
6. **Input Flexibility**: Support case-insensitive unit names and alternative unit abbreviations
7. **Batch Processing**: Support multiple conversions in single execution
8. **Help System**: Add usage instructions and supported units list