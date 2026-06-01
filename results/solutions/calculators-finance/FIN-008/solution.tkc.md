# complexcalc.tkc.md

## Overview

This program implements a command-line complex number calculator that can perform basic arithmetic operations (addition, subtraction, multiplication, division) on complex numbers. It parses complex numbers in standard mathematical notation (e.g., "3+4i", "2-5i") and outputs results in the same format.

## Architecture

The program follows a functional modular design with four main components:

- **Input Parsing Layer**: `parsecomplex()` and `parseop()` functions handle string parsing
- **Computation Layer**: `main()` performs the actual complex arithmetic using standard mathematical formulas
- **Output Formatting Layer**: `formatcomplex()` converts results back to readable string format
- **Data Flow**: Input string → operation/operand parsing → computation → formatted output

**Module Dependencies:**
- `std.io` for console I/O operations
- `std.str` for string manipulation utilities

## Key Concepts

**Toke Language Features Demonstrated:**
- **Tuple Types**: Complex numbers represented as `@($i64)` tuples storing real and imaginary parts
- **Mutable Variables**: Uses `mut` keyword for variables that change during execution
- **Pattern Matching**: Nested `if-el` chains for operation type detection
- **Standard Library Integration**: Extensive use of string and I/O stdlib functions
- **Module System**: Imports with aliasing (`i=io:std.io`, `i=s:std.str`)
- **Function Definition**: Multiple pure functions with typed parameters and return values

## Line-by-Line Notes

**Lines 1-2**: Module declaration and standard library imports with aliases for brevity

**parsecomplex() function**: 
- Handles both positive (`+`) and negative (`-`) imaginary parts separately
- Uses string slicing to remove the "i" suffix from imaginary components
- Defaults to 0 for missing real/imaginary parts

**formatcomplex() function**:
- Conditionally includes "+" sign only for positive imaginary parts
- Handles edge case where negative imaginary parts already have "-" sign

**parseop() function**:
- Searches for operation strings with surrounding spaces to avoid false matches
- Falls back to "add" as default operation

**main() function**:
- Complex multiplication uses formula: `(a+bi)(c+di) = (ac-bd)+(ad+bc)i`
- Complex division uses formula: `(a+bi)/(c+di) = [(ac+bd)+(bc-ad)i]/(c²+d²)`

## Test Coverage

To properly test this program, verify:

- **Parsing**: Various complex number formats (positive/negative, integer values)
- **Operations**: All four arithmetic operations with different operand combinations
- **Edge Cases**: Division by zero, zero operands, large numbers
- **Format Handling**: Input spacing, case sensitivity, malformed input
- **Output**: Correct mathematical results and proper formatting

## Complexity

**Time Complexity**: O(n) where n is the length of input string (dominated by string operations)

**Space Complexity**: O(n) for string manipulation and temporary array storage

**Arithmetic Operations**: O(1) for all mathematical computations

## Potential Improvements

1. **Error Handling**: Add validation for malformed input and division by zero
2. **Extended Precision**: Support floating-point complex numbers instead of integers only
3. **Enhanced Parsing**: Accept alternative complex number formats (e.g., polar form)
4. **Code Structure**: Extract common string parsing logic to reduce duplication
5. **Interactive Mode**: Support multiple calculations in a single session
6. **Advanced Operations**: Add support for exponentiation, roots, and trigonometric functions
7. **Input Validation**: Provide helpful error messages for invalid syntax
8. **Performance**: Cache parsed results for repeated operations