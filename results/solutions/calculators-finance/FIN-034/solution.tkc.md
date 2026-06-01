# lengthconv.tkc.md

## Overview

This is a unit conversion program that converts between different length measurements (millimeters, centimeters, meters, kilometers, inches, feet, yards, and miles). The program reads input from stdin in the format `<value> <from_unit> <to_unit>` and outputs the converted value with 4 decimal places precision.

## Architecture

The program follows a modular functional design with three main components:

- **Input/Output Layer**: Uses standard I/O for reading user input and displaying results
- **Conversion Engine**: Two core functions that handle bidirectional unit conversion through meters as an intermediate unit
- **Main Controller**: Orchestrates input parsing, conversion logic, and output formatting

**Data Flow**:
```
User Input → Parse → Convert to Meters → Convert from Meters → Format → Output
```

## Key Concepts

- **Module System**: Demonstrates Toke's module aliasing (`m=lengthconv`, `i=io:std.io`, `i=s:std.str`)
- **Function Definitions**: Uses `f=` syntax for function declaration with typed parameters
- **Type System**: Explicit type annotations (`$f64`, `$str`, `$i64`)
- **Conditional Logic**: Chain of `if` statements for unit matching
- **Standard Library**: Leverages `std.io` for I/O operations and `std.str` for string manipulation
- **Early Returns**: Uses `<` syntax for returning values from functions

## Line-by-Line Notes

- **Module Imports**: Three aliases are created - `m` for the module itself, `io` for I/O operations, and `s` for string utilities
- **tometers()**: Converts any supported unit to meters using multiplication factors. Returns 0.0 for unsupported units
- **frommeters()**: Converts from meters to any supported unit using division factors (implemented as multiplication by reciprocals)
- **main()**: 
  - Reads a line and splits on spaces to extract value, from-unit, and to-unit
  - Validates input has at least 3 parts before proceeding
  - Performs two-step conversion (input → meters → output unit)
  - Formats result to 4 decimal places using string formatting

## Test Coverage

The program should be tested with:
- **Valid conversions**: All unit pairs (8×8 = 64 combinations)
- **Edge cases**: Zero values, very large/small numbers
- **Invalid input**: Malformed input, unsupported units, insufficient arguments
- **Precision verification**: Ensure 4-decimal formatting works correctly
- **Round-trip accuracy**: Convert A→B→A and verify minimal precision loss

## Complexity

- **Time Complexity**: O(1) - Fixed number of conditional checks regardless of input size
- **Space Complexity**: O(1) - Uses constant memory for variables and conversions
- **Conversion Accuracy**: Limited by floating-point precision; uses standard conversion factors

## Potential Improvements

1. **Error Handling**: Add explicit error messages for invalid units or malformed input instead of silent failures
2. **Input Validation**: Validate that the first argument is actually a valid number
3. **Unit Normalization**: Make unit matching case-insensitive and support common abbreviations
4. **Precision Control**: Allow user-specified decimal places instead of hardcoded 4 digits
5. **Extended Units**: Add support for nautical miles, light-years, or other specialized length units
6. **Interactive Mode**: Support multiple conversions in a single session rather than one-shot execution
7. **Lookup Optimization**: Replace linear if-chains with hash maps for better maintainability
8. **Validation Feedback**: Return error codes from conversion functions instead of defaulting to 0.0