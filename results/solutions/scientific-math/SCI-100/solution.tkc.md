# totient.tkc.md

## Overview

This program implements Euler's totient function (φ), which calculates the number of positive integers up to n that are relatively prime to n. The program runs in an interactive loop, reading integers from standard input and outputting their totient values until an empty line is entered.

## Architecture

The program consists of three main functions organized in a single module:
- **`gcd(a, b)`** — Computes the greatest common divisor using Euclidean algorithm
- **`phi(n)`** — Implements Euler's totient function by counting relatively prime numbers
- **`main()`** — Handles I/O loop and user interaction

Data flows from user input through string parsing, mathematical computation, and formatted output back to the user.

## Key Concepts

**Type System**: Demonstrates explicit type annotations (`$i64`) for function parameters and return values, showcasing Toke's strong typing.

**Mutable Variables**: Uses `mut` keyword for variables that change during computation (`count`, `idx`).

**Standard Library Usage**: Leverages `std.io` for I/O operations and `std.str` for string manipulation and conversion.

**Control Flow**: Shows recursive function calls, conditional statements (`if`), loops (`lp`), and early returns (`<`).

**Module Imports**: Uses aliased imports (`i=io:std.io`) for cleaner code organization.

## Line-by-Line Notes

```toke
m=totient;i=io:std.io;i=s:std.str;
```
Module declaration and library imports with aliases for convenience.

```toke
f=gcd(a:$i64;b:$i64):$i64{if(b=0){<a};<gcd(b;a%b)};
```
Recursive GCD implementation using Euclidean algorithm with early return syntax.

```toke
let count=mut.0;let idx=mut.1;
```
Initialize mutable counters for the totient calculation loop.

```toke
lp(idx<n){if(gcd(idx;n)=1){count=count+1};idx=idx+1};
```
Main counting loop that checks each number from 1 to n-1 for relative primality.

```toke
lp(1=1){...br};
```
Infinite loop pattern (`1=1` always true) with explicit break condition.

## Test Coverage

To thoroughly test this program, verify:
- **Edge Cases**: φ(1) = 1, small primes like φ(2) = 1, φ(3) = 2
- **Composite Numbers**: φ(6) = 2, φ(8) = 4, φ(12) = 4
- **Prime Numbers**: φ(p) = p-1 for any prime p
- **Input Validation**: Empty line termination, invalid input handling
- **Large Numbers**: Performance with moderately large inputs

## Complexity

**Time Complexity**: O(n log log n) per query due to the nested GCD calls within the counting loop.

**Space Complexity**: O(log min(a,b)) due to recursive GCD call stack depth.

The current implementation has poor scalability for large n values due to the brute-force counting approach.

## Potential Improvements

1. **Algorithmic Optimization**: Replace brute-force counting with prime factorization formula: φ(n) = n × ∏(1 - 1/p) for all prime factors p.

2. **Input Validation**: Add error handling for non-numeric input and negative numbers.

3. **Performance**: Implement iterative GCD to reduce call stack usage.

4. **Code Structure**: Extract string formatting logic into a separate function for better readability.

5. **Caching**: For interactive use, cache results of previously computed totient values.

6. **Extended Range**: Consider supporting larger integer types if available in the Toke standard library.