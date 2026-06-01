# Mortgage Payment Calculator - Companion Documentation

## Overview

This toke program calculates monthly mortgage payments using the standard amortization formula. It reads loan parameters from standard input (principal, annual percentage rate, and loan term in years) and outputs the calculated monthly payment amount formatted to two decimal places.

## Architecture

The program follows a simple modular structure:

- **Module Declaration**: `mortgage` module with imported standard libraries
- **Core Function**: `payment()` implements the mortgage calculation formula
- **Main Function**: `main()` handles I/O, input parsing, and orchestrates the calculation
- **Data Flow**: stdin → parsing → calculation → formatted output

**Dependencies:**
- `std.io` - Input/output operations
- `std.str` - String manipulation and type conversion
- `std.math` - Mathematical operations (power function)

## Key Concepts

**Toke Language Features Demonstrated:**
- Module system and library imports with aliasing
- Function definitions with typed parameters and return values
- Type system usage (`$f64`, `$i64`)
- String operations (splitting, parsing, formatting)
- Mathematical computations with floating-point precision
- Standard library integration

**Type Safety:** All functions use explicit type annotations ensuring compile-time type checking.

## Line-by-Line Notes

```toke
m=mortgage;i=io:std.io;i=s:std.str;i=math:std.math;
```
Module declaration and library imports with short aliases for convenience.

```toke
let r=rate/12.0;let n=s.tofloat(s.fromint(years*12));
```
Converts annual rate to monthly rate; converts total months (int) to float via string conversion for math operations.

```toke
let tmp=math.pow(1.0+r;n);let monthly=principal*r*tmp/(tmp-1.0);
```
Implements the standard mortgage formula: `M = P * r * (1+r)^n / ((1+r)^n - 1)` where M=monthly payment, P=principal, r=monthly rate, n=number of payments.

```toke
let parts=s.split(line;" ");if(parts.len()>=3){...}
```
Parses space-separated input with basic validation (minimum 3 fields required).

```toke
io.println(s.format(result;"%.2f"))
```
Outputs result formatted as currency with 2 decimal places.

## Test Coverage

**Recommended Test Cases:**
- Standard 30-year mortgage calculation
- Different interest rates (0%, low rates, high rates)
- Various loan terms (15, 20, 30 years)
- Edge cases: very small/large principal amounts
- Input validation: insufficient parameters, invalid numbers
- Boundary conditions: zero interest rate

**Example Test Input:** `200000 0.045 30` (200k principal, 4.5% APR, 30 years)

## Complexity

**Time Complexity:** O(1) - Constant time for mathematical calculation
**Space Complexity:** O(n) where n is the length of input line (for string operations)

The `math.pow()` operation dominates computational cost but remains constant relative to input size.

## Potential Improvements

1. **Input Validation**: Add error handling for invalid numeric inputs and negative values
2. **Output Enhancement**: Include loan summary (total interest paid, total amount)
3. **Format Flexibility**: Support different input formats (CSV, JSON) and currency symbols
4. **Precision**: Consider using decimal arithmetic for financial calculations instead of floating-point
5. **Interactive Mode**: Allow multiple calculations without restarting the program
6. **Documentation**: Add inline comments for formula explanation
7. **Edge Cases**: Handle zero/negative interest rates with appropriate logic
8. **Code Style**: Break long lines for better readability and add proper spacing