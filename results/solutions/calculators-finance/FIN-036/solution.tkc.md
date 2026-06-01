# Speed Converter Program Documentation (.tkc.md)

## Overview

This Toke program implements a command-line speed unit converter that transforms velocity measurements between different units (km/h, mph, knots, mach). The program reads input from stdin, parses the value and units, performs the conversion via meters per second as an intermediate unit, and outputs the formatted result.

## Architecture

The program consists of two main components:
- **`convert` function**: Core conversion logic that uses meters per second (mps) as a universal intermediate unit
- **`main` function**: Input/output handling and user interface logic

**Data flow**: Input parsing → Unit validation → Conversion to mps → Conversion to target unit → Formatted output

The architecture follows a standard conversion pattern where all units are normalized to a common base (mps) before converting to the target unit.

## Key Concepts

- **Module imports**: Demonstrates aliasing with `m=convert`, `i=io:std.io`, `i=s:std.str`
- **Function definitions**: Shows parameter typing with `$f64`, `$str` and return types
- **Conditional logic**: Nested `if-el` chains for unit selection
- **Mutable variables**: Uses `mut.val` for intermediate calculations
- **String operations**: String splitting, parsing, and formatting
- **Array/collection access**: Uses `.get()` method and `.len()` property
- **Early returns**: Uses `<` operator for function returns

## Line-by-Line Notes

**Module imports**: Creates aliases for convert module, standard I/O, and string utilities.

**Lines in convert function**:
- Same unit check: `if(from=to){<val}` - Returns original value if no conversion needed
- mps initialization: `let mps=mut.val` - Creates mutable variable for intermediate calculations
- Nested conditionals: Convert input unit to meters per second using standard conversion factors
- Output conversion: Transform mps to target unit using inverse operations where applicable

**Lines in main function**:
- Input parsing: Splits input line on spaces to extract value, from-unit, and to-unit
- Validation: Checks for minimum 3 parts before proceeding
- Type conversion: `s.tofloat()` converts string to floating-point number
- Output formatting: Uses `%.4f` format specifier for 4 decimal places

## Test Coverage

The program should be tested with:
- **Valid conversions**: Each unit pair combination (kmh↔mph, knots↔mach, etc.)
- **Same unit**: Verify identity conversion works correctly
- **Edge cases**: Zero values, very large/small numbers
- **Invalid input**: Insufficient parameters, malformed numbers, unknown units
- **Boundary conditions**: Extreme values that might cause precision issues

## Complexity

- **Time complexity**: O(1) - Fixed number of conditional checks regardless of input size
- **Space complexity**: O(1) - Uses constant additional memory for variables
- **Precision**: Limited by floating-point arithmetic; mach conversion assumes standard conditions (343 m/s)

## Potential Improvements

1. **Error handling**: Add validation for unknown units and malformed input
2. **Unit flexibility**: Support case-insensitive unit names and abbreviations
3. **Precision**: Use more accurate conversion factors (especially for mach which varies with temperature/altitude)
4. **Code structure**: Extract unit conversion factors into constants/lookup table
5. **Help system**: Add usage instructions for invalid input
6. **Batch processing**: Support multiple conversions in a single run
7. **Additional units**: Extend to support feet/second, kilometers/second, etc.
8. **Output formatting**: Make decimal precision configurable
9. **Input validation**: Verify numeric input before conversion attempts