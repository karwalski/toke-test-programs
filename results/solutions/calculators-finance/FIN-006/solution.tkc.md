# baseconv.tkc.md

## Overview

This Toke program implements a general-purpose number base conversion utility that can convert numbers between any bases from 2-36. The program reads input in the format "number source_base target_base" and outputs the converted number using alphanumeric characters (0-9, A-Z) to represent digits.

## Architecture

The program is structured as a functional module with six main components:

- **Character conversion functions**: `chartoint()` and `inttochar()` for mapping between characters and numeric values
- **Mathematical utilities**: `power()` for exponentiation 
- **Base conversion logic**: `todecimal()` and `frombase10()` for two-stage conversion
- **Main program**: `main()` handles I/O and orchestrates the conversion process

**Data flow**: Input string → Parse components → Convert to decimal → Convert to target base → Output result

## Key Concepts

- **Function definitions**: Demonstrates Toke's `f=name(params):type{body}` syntax
- **Module imports**: Uses `std.io` for I/O and `std.str` for string operations
- **Type annotations**: Explicit `$i64` and `$str` type declarations
- **Mutable variables**: `let var=mut.value` pattern for variables that change
- **String manipulation**: Slicing, concatenation, splitting, and parsing
- **Control flow**: Extensive use of `if` statements and `lp` (loop) constructs
- **Early returns**: `<value` syntax for function returns

## Line-by-Line Notes

**Character mapping functions**: Both `chartoint()` and `inttochar()` use exhaustive if-chains to map 0-9 and A-Z, supporting bases up to 36. Default fallback returns 0 or "0".

**Power function**: Implements integer exponentiation using a simple multiplication loop since Toke lacks built-in power operators.

**Base conversion strategy**: Uses two-phase conversion (source→decimal→target) rather than direct conversion, simplifying the algorithm at the cost of an intermediate step.

**Modulo operation**: `val-val/base*base` implements modulo since Toke appears to lack a native modulo operator.

**Input parsing**: Expects space-separated input with exactly three components, with basic error handling.

## Test Coverage

The program should be tested with:
- **Basic conversions**: Binary↔decimal, decimal↔hexadecimal
- **Edge cases**: Base 2 (minimum), base 36 (maximum), single digit numbers
- **Zero handling**: Conversion of "0" between different bases
- **Error conditions**: Invalid input format, unsupported characters
- **Large numbers**: Testing numerical limits and overflow behavior

## Complexity

**Time Complexity**: O(n) where n is the number of digits in the input number
**Space Complexity**: O(n) for string storage and manipulation

The character mapping functions have O(1) lookup time but could be optimized. The power function adds O(d) complexity where d is the digit position.

## Potential Improvements

1. **Lookup tables**: Replace if-chains with arrays or hash maps for O(1) character conversion
2. **Input validation**: Add checks for invalid characters relative to the source base
3. **Error handling**: More specific error messages and graceful failure modes
4. **Direct conversion**: Implement single-pass conversion for better efficiency
5. **Code formatting**: Add whitespace and structure for better readability
6. **Range checking**: Validate that bases are within the supported 2-36 range
7. **Negative number support**: Extend functionality to handle negative values