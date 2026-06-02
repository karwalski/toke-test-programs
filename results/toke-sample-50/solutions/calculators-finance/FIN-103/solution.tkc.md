# primecheck.tkc.md

## Overview

This program implements a primality test that checks whether a user-provided integer is prime or composite. It uses an optimized trial division algorithm that only tests odd divisors up to the square root of the input number.

## Architecture

**Module Structure:**
- **Main module:** `primecheck`
- **Dependencies:** `std.io`, `std.str`, `std.math`

**Function Layout:**
- `isprime(n: $i64): $bool` - Core primality testing logic
- `main(): $i64` - User interface and program entry point

**Data Flow:**
1. Read user input as string → Convert to integer → Test primality → Output result

## Key Concepts

**Toke Language Features Demonstrated:**
- **Module system:** Import aliasing (`i=io:std.io`, `i=s:std.str`)
- **Type system:** Explicit type annotations (`$i64`, `$bool`, `$f64`)
- **Type casting:** `as$f64` and `as$i64` conversions
- **Mutable variables:** `mut.3` for loop counter
- **Control flow:** `if/el` conditionals, `lp` loops
- **Early returns:** `<false`, `<true` pattern
- **Standard library:** Math operations, I/O, string conversion

## Line-by-Line Notes

**isprime() function:**
- `if(n<2){<false}` - Handle edge cases (0, 1, negatives)
- `let rem=n-n/2*2` - Manual modulo operation to check even numbers
- `let limit=math.sqrt(n as$f64)as$i64` - Optimization: only check up to √n
- `let idx=mut.3` - Start trial division from 3 (first odd number after 2)
- `lp(idx<=limit)` - Loop while index ≤ square root
- `let r=n-n/idx*idx` - Manual modulo to test divisibility
- `idx=idx+2` - Increment by 2 to test only odd numbers

**main() function:**
- `let n=s.toint(io.readln())` - Read and parse user input
- Conditional output based on primality test result

## Test Coverage

**Edge Cases Handled:**
- Numbers less than 2 (return false)
- Number 2 (special case, return true)
- Even numbers > 2 (return false immediately)
- Odd composites (detected by trial division)
- Prime numbers (pass all divisibility tests)

**Input Ranges:**
- Supports all 64-bit signed integers
- Handles negative inputs correctly (classified as non-prime)

## Complexity

**Time Complexity:** O(√n)
- Best case: O(1) for n < 2, n = 2, or even n > 2
- Average/Worst case: O(√n) for odd numbers requiring full trial division

**Space Complexity:** O(1)
- Uses only a constant amount of additional memory regardless of input size

## Potential Improvements

1. **Algorithm Optimization:**
   - Implement Sieve of Eratosthenes for multiple queries
   - Add Miller-Rabin probabilistic test for very large numbers

2. **Code Quality:**
   - Add input validation and error handling for invalid strings
   - Extract magic numbers (2, 3) into named constants
   - Add comprehensive test suite with known primes/composites

3. **Performance:**
   - Use built-in modulo operator if available (`%`)
   - Consider wheel factorization (skip multiples of 2,3,5)
   - Cache square root calculation outside loop

4. **User Experience:**
   - Add input prompts and usage instructions
   - Support batch processing of multiple numbers
   - Provide factorization for composite numbers