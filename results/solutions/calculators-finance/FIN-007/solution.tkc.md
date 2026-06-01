# Fraction Calculator - Companion Documentation

## Overview

This toke program implements a command-line fraction calculator that performs basic arithmetic operations (addition, subtraction, multiplication, division) on fractions. It parses input in the format "num1/den1 operator num2/den2" and outputs the result as a reduced fraction or whole number.

## Architecture

The program is structured as a single module `frac` with four main functions:

- **`gcd()`** — Computes greatest common divisor using Euclidean algorithm
- **`reduce()`** — Reduces fractions to lowest terms and handles sign normalization
- **`parsefrac()`** — Parses string representation of fractions into numerator/denominator tuples
- **`main()`** — Orchestrates input parsing, operation execution, and output formatting

**Data Flow:** Input string → Parse fractions → Apply operation → Reduce result → Format output

## Key Concepts

- **Tuple Types:** Uses `@($i64)` tuples to represent fractions as (numerator, denominator) pairs
- **String Manipulation:** Leverages `std.str` for splitting, trimming, and type conversion
- **Conditional Logic:** Nested if-else chains for operation dispatch and output formatting
- **Mutable Variables:** Uses `mut` keyword for result accumulation variables
- **Standard Library:** Imports `std.io` and `std.str` for I/O and string operations

## Line-by-Line Notes

**Module Imports:** `m=frac;i=io:std.io;i=s:std.str` sets up module namespace and library aliases

**GCD Implementation:** Recursive Euclidean algorithm with base case `b=0`

**Sign Normalization:** In `reduce()`, negative denominators are converted to negative numerators for canonical form

**Tuple Access:** Uses `.get(0)` and `.get(1)` to extract numerator and denominator from tuples

**Operation Logic:** 
- Addition/Subtraction: Cross-multiply to common denominator
- Multiplication: Multiply numerators and denominators directly  
- Division: Multiply by reciprocal of second fraction

**Output Formatting:** Whole numbers (denominator = 1) are displayed without fraction notation

## Test Coverage

The program should be tested with:
- Basic operations: `1/2 + 1/3`, `3/4 - 1/2`, `2/3 * 3/5`, `1/2 / 1/4`
- Negative fractions: `-1/2 + 1/3`, `1/2 - 3/4`
- Whole numbers: `2/1 + 3/1`
- Fractions requiring reduction: `2/4 + 3/6`
- Edge cases: Division by zero, malformed input

## Complexity

- **Time Complexity:** O(log(min(a,b))) for GCD computation via Euclidean algorithm
- **Space Complexity:** O(log(min(a,b))) due to recursive GCD calls
- **Overall:** Linear in input size for parsing, dominated by GCD computation

## Potential Improvements

1. **Error Handling:** Add validation for division by zero and malformed input
2. **Input Validation:** Check for invalid denominators and non-numeric input
3. **Mixed Numbers:** Support input/output in mixed number format (e.g., "1 1/2")
4. **Iterative GCD:** Replace recursive GCD with iterative version to reduce stack usage
5. **Operator Precedence:** Support parentheses and multiple operations in single expression
6. **Decimal Support:** Add conversion between fraction and decimal representations