# Calculator Program Documentation (calc.tkc.md)

## Overview
This is a command-line calculator program that performs basic mathematical operations on single numeric inputs. The program reads a line of input containing an operation name and a number, then outputs the calculated result formatted to 6 decimal places.

## Architecture
The program follows a simple linear architecture:
- **Module**: `calc` (single-module program)
- **Imports**: Standard library modules for I/O (`std.io`), string manipulation (`std.str`), and mathematical functions (`std.math`)
- **Entry Point**: `main()` function returning `i64`
- **Data Flow**: Input → Parse → Calculate → Format → Output

## Key Concepts
- **Module System**: Demonstrates Toke's module import syntax with aliasing (`i=io:std.io`)
- **Standard Library Usage**: Leverages stdlib for I/O, string operations, and math functions
- **Type System**: Shows string-to-float conversion and mutable variable declaration
- **Conditional Logic**: Nested if-else chains for operation selection
- **String Formatting**: Uses format strings for numeric output precision

## Line-by-Line Notes

```toke
m=calc;
```
Module declaration establishing `calc` namespace.

```toke
i=io:std.io;i=s:std.str;i=math:std.math;
```
Import statements with aliases: `io` for I/O operations, `s` for string utilities, `math` for mathematical functions.

```toke
let parts=s.split(line;" ");
```
Splits input line on space character to separate operation from operand.

```toke
let result=mut.0.0;
```
Declares mutable float variable initialized to 0.0 for storing calculation results.

```toke
if(op="sin"){result=math.sin(val)}el{...}
```
Nested conditional chain checking operation type and calling corresponding math function.

```toke
io.println(s.format(result;"%.6f"));
```
Outputs result formatted to 6 decimal places using printf-style formatting.

## Test Coverage
To properly test this program, verify:
- **Valid Operations**: Test each supported operation (sin, cos, sqrt, ln, log) with various inputs
- **Edge Cases**: Empty input, single argument, non-numeric values
- **Mathematical Boundaries**: Negative values for sqrt, zero/negative for logarithms
- **Format Verification**: Ensure 6-decimal precision in output
- **Invalid Operations**: Unknown operation names should default to 0.0

## Complexity
- **Time Complexity**: O(1) - All operations are constant time
- **Space Complexity**: O(n) where n is input line length (for string splitting)
- **Performance**: Minimal overhead, suitable for interactive use

## Potential Improvements

1. **Error Handling**: Add validation for invalid inputs and mathematical errors (e.g., sqrt of negative numbers)
2. **Extended Operations**: Support additional functions (tan, exp, power, etc.)
3. **Multi-argument Support**: Enable operations requiring two operands (add, multiply, power)
4. **Input Validation**: Check for proper number format before conversion
5. **Help System**: Display available operations when invalid input is provided
6. **Precision Control**: Allow user to specify output decimal precision
7. **Expression Parsing**: Support full mathematical expressions instead of single operations
8. **Return Code**: Use meaningful exit codes instead of hardcoded `<0`