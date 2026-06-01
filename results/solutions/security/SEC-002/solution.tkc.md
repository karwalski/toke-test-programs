# passwordstrength.tkc.md

## Overview

This Toke program analyzes password strength by evaluating multiple criteria including length, character diversity, and symbol usage. It reads a password from standard input and outputs a strength rating of "weak", "strong", or "very_strong" based on a scoring system.

## Architecture

The program is structured as a single module `passwordstrength` with five functions:

- **Character Detection Functions**: `haslower()`, `hasupper()`, `hasdigit()`, `hassym()` - Each scans the password for specific character types
- **Main Controller**: `main()` - Orchestrates the scoring logic and output generation
- **Data Flow**: Input → Character analysis → Score accumulation → Classification → Output

The architecture follows a functional decomposition pattern where each character type check is isolated into its own pure function.

## Key Concepts

**Toke Language Features Demonstrated:**
- **Module system**: Uses `std.io` and `std.str` standard library modules
- **Type annotations**: Explicit `$str`, `$bool`, `$i64` type declarations
- **Mutable variables**: `mut.false`, `mut.0` for state that changes during execution
- **String manipulation**: `s.slice()`, `s.contains()`, `s.len()`, `s.trim()`
- **Control flow**: `lp()` loops, conditional `if/el` chains
- **Function composition**: Breaking complex logic into reusable components

## Line-by-Line Notes

**Module imports**: `i=io:std.io;i=s:std.str` - Note the variable shadowing where `i` is rebound from `io` to `s`

**Character detection pattern**: Each `has*()` function follows identical logic:
1. Get string length
2. Initialize mutable boolean flag
3. Loop through each character using `s.slice(p;i;i+1)`
4. Check if character exists in hardcoded character set using `s.contains()`
5. Return found status

**Scoring system in main()**:
- Length ≥8: +1 point
- Length ≥16: +1 point (bonus)
- Has lowercase: +1 point
- Has uppercase: +1 point
- Has digits: +1 point
- Has symbols: +1 point

**Classification thresholds**:
- Score ≥6: "very_strong"
- Score ≥4: "strong" 
- Score <4: "weak"

## Test Coverage

Recommended test cases should verify:
- **Length variations**: Short (<8), medium (8-15), long (≥16) passwords
- **Character type combinations**: Single type, mixed types, all types
- **Edge cases**: Empty strings, whitespace handling, Unicode characters
- **Boundary conditions**: Exactly 8/16 characters, score thresholds (3,4,5,6 points)
- **Symbol set coverage**: Each symbol in `!@#$%^&*()-_+=.,;:?/`

## Complexity

- **Time Complexity**: O(n×m) where n = password length, m = character set size (worst case O(n×26) for alphabet checks)
- **Space Complexity**: O(1) - only stores scalar variables and single characters
- **Performance Note**: The character detection could be optimized since each function rescans the entire string

## Potential Improvements

1. **Performance Optimization**: Single-pass character analysis instead of 4 separate scans
2. **Character Set Efficiency**: Use character code ranges instead of string containment checks
3. **Unicode Support**: Handle international characters and emoji properly
4. **Configurable Scoring**: Extract scoring weights and thresholds to configuration
5. **Enhanced Validation**: Check for common patterns, dictionary words, repetition
6. **Error Handling**: Validate input and handle I/O errors gracefully
7. **Code Reuse**: Create generic `hascharset(password, charset)` function to eliminate duplication
8. **Extended Metrics**: Add entropy calculation, pattern detection, or NIST guideline compliance