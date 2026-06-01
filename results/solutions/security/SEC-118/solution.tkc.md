# Password Hashing Strength Analyzer - Companion Documentation

## Overview

This toke program analyzes password hashing configurations to determine if they use cryptographically strong key derivation functions (KDFs). It reads a KDF name and configuration from standard input, then evaluates the strength based on modern security standards and outputs either "strong" or "weak".

## Architecture

The program follows a simple linear architecture:
- **Input Module**: Uses `std.io` for reading KDF name and configuration
- **String Processing**: Leverages `std.str` for string manipulation and matching
- **Analysis Logic**: Sequential conditional checks for known strong KDFs
- **Output Module**: Binary classification output via `std.io`

**Data Flow**: `stdin` → `string processing` → `kdf evaluation` → `strength classification` → `stdout`

## Key Concepts

- **Module Aliasing**: Demonstrates toke's module import system with aliases (`io:std.io`, `s:std.str`)
- **Function Definition**: Shows function syntax with typed parameters and return values
- **Mutable Variables**: Uses `mut.false` for mutable boolean state
- **String Operations**: Utilizes standard library string functions (`trim`, `contains`)
- **Conditional Logic**: Implements branching with `if/el` statements
- **Type System**: Explicit type annotations (`$str`, `$bool`, `$i64`)

## Line-by-Line Notes

```toke
m=sec;i=io:std.io;i=s:std.str;
```
Module imports with aliasing - note the reuse of variable `i` for multiple imports.

```toke
f=contains(line:$str;sub:$str):$bool{<s.contains(line;sub)}
```
Wrapper function around standard library's string contains - the `<` operator returns the expression result.

```toke
let kdf=s.trim(io.readln());let cfg=io.readln();
```
Input reading with string trimming for the KDF name, raw configuration string.

```toke
if(contains(kdf;"pbkdf2")){let hasiter=contains(cfg;"100000");if(hasiter=true){strong=true}}
```
Special case for PBKDF2 - only considered strong with ≥100,000 iterations.

## Test Coverage

Recommended test cases should verify:
- **Strong KDFs**: argon2, scrypt, bcrypt recognition
- **Conditional Strength**: PBKDF2 with sufficient iterations (≥100,000)
- **Weak Configurations**: PBKDF2 with low iterations, unknown KDFs
- **Edge Cases**: Empty input, malformed configuration strings
- **Case Sensitivity**: Mixed case KDF names
- **Whitespace Handling**: Leading/trailing spaces in KDF names

## Complexity

- **Time Complexity**: O(n) where n is the length of input strings (dominated by string search operations)
- **Space Complexity**: O(1) excluding input storage (only stores boolean flags and string references)
- **I/O Operations**: 2 reads, 1 write - minimal I/O overhead

## Potential Improvements

1. **Case-Insensitive Matching**: Add string normalization for KDF names
2. **Configuration Parsing**: Implement proper config parsing instead of simple substring search
3. **Extensible KDF Database**: Move KDF definitions to external configuration or data structure
4. **Detailed Feedback**: Provide specific recommendations for weak configurations
5. **Input Validation**: Add error handling for malformed input
6. **Parameterized Thresholds**: Make iteration count threshold configurable
7. **Additional KDFs**: Support for newer algorithms like Balloon hashing or additional Argon2 variants
8. **Security Context**: Consider salt requirements and other security parameters beyond just algorithm choice