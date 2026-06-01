# modinv.tkc.md

## Overview

This Toke program computes the modular multiplicative inverse of a number using the Extended Euclidean Algorithm. It reads two integers from standard input and outputs either the modular inverse or "NO_INVERSE" if no inverse exists.

## Architecture

The program consists of three main functions in a single module:

- **`extgcd`** — Core recursive implementation of the Extended Euclidean Algorithm
- **`modinv`** — Wrapper that extracts the modular inverse from the extended GCD result
- **`main`** — I/O handler that parses input and formats output

Data flows from input parsing → inverse calculation → result formatting, with the mathematical computation isolated in pure functions.

## Key Concepts

- **Custom Types**: Defines `$triple` struct to return multiple values from GCD computation
- **Recursion**: Uses tail-recursive pattern for the Extended Euclidean Algorithm
- **Standard Library**: Leverages `std.io` for I/O operations and `std.str` for string manipulation
- **Error Handling**: Returns sentinel value (-1) when inverse doesn't exist
- **Module Aliases**: Demonstrates Toke's module aliasing with shortened identifiers

## Line-by-Line Notes

```toke
t=$triple{gcd:$i64;x:$i64;y:$i64}
```
Defines a struct to hold the extended GCD result: the GCD value and Bézout coefficients.

```toke
f=extgcd(a:$i64;b:$i64):$triple{if(b=0){<$triple{gcd:a;x:1;y:0}}
```
Base case: when `b=0`, GCD is `a` with coefficients `x=1, y=0`.

```toke
let q=a/b;let r=a-q*b;let result=extgcd(b;r)
```
Euclidean division step, then recursive call with swapped parameters.

```toke
<$triple{gcd:result.gcd;x:result.y;y:result.x-q*result.y}
```
Backtracking step that updates Bézout coefficients using the quotient.

```toke
if(result.x<0){<result.x+m}
```
Ensures the returned inverse is positive by adding the modulus.

## Test Coverage

The program should be tested with:
- **Valid cases**: Coprime integers (e.g., `3 11` → `4`)
- **Invalid cases**: Non-coprime integers (e.g., `6 9` → `NO_INVERSE`)
- **Edge cases**: `a=1`, large numbers, negative inputs
- **Boundary conditions**: When `a ≥ m` or `a = 0`

## Complexity

- **Time**: O(log min(a,m)) — logarithmic due to Euclidean algorithm efficiency
- **Space**: O(log min(a,m)) — recursion depth proportional to number of divisions

## Potential Improvements

1. **Input Validation**: Add bounds checking and handle malformed input gracefully
2. **Iterative Implementation**: Replace recursion with iteration to reduce stack usage
3. **Error Types**: Use proper error types instead of sentinel values
4. **Documentation**: Add inline comments explaining the mathematical concepts
5. **Optimization**: Handle common cases (like `a=1`) directly without full algorithm
6. **Extended Interface**: Support batch processing of multiple inverse calculations