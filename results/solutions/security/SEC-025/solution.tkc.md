# audit.tkc.md

## Overview

This Toke program implements a security audit tool that analyzes password hashing algorithms from CSV input. It reads lines from standard input, parses each line to extract hashing algorithm information, and flags potential security vulnerabilities like weak algorithms (MD5, SHA1) or low-cost bcrypt configurations.

## Architecture

The program follows a simple two-function architecture:

- **`checkline()`** — Core validation logic that parses and analyzes individual CSV records
- **`main()`** — Input/output controller that orchestrates line reading and result reporting

Data flows linearly: stdin → line parsing → security validation → result accumulation → stdout reporting.

## Key Concepts

- **String manipulation**: Extensive use of `std.str` for parsing (`split`, `trim`, `slice`, `toint`)
- **Early returns**: Toke's `<` operator for function exit with return values
- **Mutable variables**: `mut` keyword for state that changes during execution
- **Control flow**: `lp(true)` infinite loop with explicit `br` (break) statements
- **Error handling**: Implicit validation through length checks and algorithm comparison

## Line-by-Line Notes

```toke
m=audit;i=io:std.io;i=s:std.str
```
Module declaration and imports with aliasing for cleaner code.

```toke
let parts=s.split(line;",");if(parts.len()<3){<"ok"}
```
CSV parsing with early validation—assumes malformed records are acceptable.

```toke
let hash=parts.get(1);let algo=s.trim(parts.get(2))
```
Extracts hash value and algorithm name, trimming whitespace from algorithm field.

```toke
if(algo="bcrypt"){let cost=s.slice(hash;4;6);let c=s.toint(cost);if(c<10){<"low_cost"}
```
bcrypt-specific validation: extracts cost parameter from positions 4-6 in hash string and flags costs below 10 as insufficient.

```toke
let result=mut."ok";lp(true){...;if(r!="ok"){result=r;br;}
```
State machine pattern: continues processing until first security issue found, then exits with that specific violation.

## Test Coverage

The program should be tested with:

- **Malformed CSV**: Lines with <3 fields
- **Weak algorithms**: MD5 and SHA1 detection
- **bcrypt cost analysis**: Various cost levels (especially 8-12 range)
- **Edge cases**: Empty lines, whitespace handling, malformed bcrypt hashes
- **Clean data**: Valid modern hashing configurations

## Complexity

- **Time**: O(n×m) where n = number of input lines, m = average line length (due to string operations)
- **Space**: O(m) for string processing of individual lines
- **Early termination**: Best case O(1) if first line contains a security issue

## Potential Improvements

1. **Error handling**: Add validation for malformed bcrypt hashes and invalid cost extraction
2. **Algorithm coverage**: Support for additional algorithms (Argon2, PBKDF2, scrypt)
3. **Configurable thresholds**: Make bcrypt cost threshold adjustable via command-line arguments
4. **Detailed reporting**: Return line numbers and specific violation details instead of just the first error type
5. **Input validation**: Robust CSV parsing to handle quoted fields and escaped commas
6. **Performance**: Consider streaming validation for large audit files
7. **Standards compliance**: Align cost recommendations with current OWASP guidelines