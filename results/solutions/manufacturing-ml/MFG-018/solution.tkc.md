# defectrate.tkc.md

## Overview

This program calculates Six Sigma quality metrics from manufacturing defect data. It reads CSV input containing units, defects, and opportunities per unit, then computes DPMO (Defects Per Million Opportunities) and the corresponding sigma level with a 1.5-sigma shift adjustment.

## Architecture

The program follows a functional architecture with mathematical utility functions supporting a main data processing pipeline:

```
Mathematical Functions:
├── power() - Integer exponentiation
├── mysqrt() - Newton's method square root
├── myexp() - Taylor series exponential
├── absf() - Absolute value
├── normcdf() - Normal CDF approximation
├── invnorm() - Inverse normal via bisection
└── roundn() - Decimal place rounding

Main Pipeline:
main() → CSV parsing → DPMO calculation → Sigma level → JSON output
```

## Key Concepts

- **Custom Math Implementation**: Demonstrates implementing mathematical functions from scratch using basic loops and arithmetic
- **Type Casting**: Extensive use of `as$f64` and `as$i64` for numeric conversions
- **Mutable Variables**: Uses `mut.` prefix for variables that change during computation
- **String Manipulation**: Leverages `std.str` for parsing and formatting
- **Conditional Logic**: Six Sigma domain logic with proper error handling

## Line-by-Line Notes

**Module Imports (Line 1)**:
```toke
m=defectrate;i=io:std.io;i=s:std.str;
```
- Unusual double assignment to `i` - second assignment shadows the first
- Should use distinct variable names for io and string modules

**Mathematical Functions**:
- `power()`: Simple integer exponentiation with O(n) loop
- `mysqrt()`: Newton-Raphson method with fixed 20 iterations
- `myexp()`: Taylor series with 30 terms for e^x approximation
- `normcdf()`: Abramowitz-Stegun polynomial approximation for standard normal CDF
- `invnorm()`: Binary search with 100 iterations for inverse normal

**Main Processing**:
```toke
let dpmo=defects/(units*opp)*1000000.0;
let sigma=z+1.5;
```
- DPMO calculation follows standard Six Sigma formula
- 1.5-sigma shift is industry standard adjustment for process drift

**JSON Output Construction**:
Manual string concatenation builds JSON response due to lack of native JSON support.

## Test Coverage

The program should be tested with:
- **Valid CSV Input**: "units,defects,opportunities\n100,5,10" 
- **Edge Cases**: Zero defects, single unit, high defect rates
- **Invalid Input**: Malformed CSV, non-numeric values, insufficient columns
- **Mathematical Bounds**: Very small/large DPMO values that stress the inverse normal function

## Complexity

- **Time Complexity**: O(1) with fixed iteration counts in mathematical functions
- **Space Complexity**: O(n) where n is the length of input strings (CSV parsing)
- **Numerical Stability**: Limited by fixed iteration counts and floating-point precision

## Potential Improvements

1. **Module Import Fix**: Use distinct variable names (`io` and `str`) instead of shadowing
2. **Error Handling**: Add validation for negative values and division by zero
3. **Mathematical Accuracy**: 
   - Increase iteration counts for better precision
   - Add convergence checks instead of fixed iterations
   - Use more accurate polynomial coefficients for normal CDF
4. **Code Structure**: Extract calculation logic into separate functions for better testability
5. **JSON Handling**: Use a proper JSON library if available
6. **Input Validation**: Verify CSV format and data types before processing
7. **Performance**: Cache expensive calculations like the normal CDF polynomial