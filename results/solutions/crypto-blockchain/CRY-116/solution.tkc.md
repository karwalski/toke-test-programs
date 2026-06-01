# hexcompare.tkc.md

## Overview

This program compares two strings character by character to determine if they are identical. It reads two input strings, trims whitespace, and performs a detailed comparison that accounts for both length differences and character mismatches, ultimately outputting either "EQUAL" or "NOT_EQUAL".

## Architecture

**Single Module Structure:**
- **Module**: `hexcompare`
- **Main Function**: `main()` - handles the entire comparison workflow
- **Dependencies**: 
  - `std.io` (aliased as `io`) - for input/output operations
  - `std.str` (aliased as `s`) - for string manipulation

**Data Flow:**
1. Input acquisition → String preprocessing → Length analysis → Character-by-character comparison → Result output

## Key Concepts

**Toke Language Features Demonstrated:**
- **Module imports and aliasing** (`i=io:std.io`, `i=s:std.str`)
- **Mutable variables** (`mut` keyword for `diff`, `n`, `idx`)
- **String operations** (trim, length, slicing, contains)
- **Control flow** (conditional statements, loops)
- **Type annotations** (`$i64` return type)
- **Standard library usage** (I/O and string utilities)

## Line-by-Line Notes

**Variable Initialization:**
```toke
let a=s.trim(io.readln());let b=s.trim(io.readln())
```
Reads two lines of input and removes leading/trailing whitespace.

**Length Comparison Logic:**
```toke
let n=mut.la;if(lb<la){n=lb}
```
Sets comparison boundary to the shorter string length to prevent index overflow.

**Character Comparison:**
```toke
if(s.contains(ca;cb)=false){diff=diff+1}
```
Uses `contains()` for character matching rather than direct equality - this is an unusual approach that may have unintended behavior since `contains()` checks substring presence, not equality.

**Loop Structure:**
```toke
lp(idx<n){...;idx=idx+1}
```
Manual index-based iteration through characters using `lp` (loop) construct.

## Test Coverage

**Scenarios to Verify:**
- **Equal strings**: Same content and length → "EQUAL"
- **Different lengths**: Strings of varying sizes → "NOT_EQUAL"
- **Same length, different content**: Character mismatches → "NOT_EQUAL"
- **Whitespace handling**: Leading/trailing spaces properly trimmed
- **Edge cases**: Empty strings, single characters

## Complexity

**Time Complexity:** O(min(m,n)) where m and n are the lengths of input strings
**Space Complexity:** O(m+n) for storing the input strings and their slices

The algorithm performs a single pass through the shorter string, making it linear in the minimum length.

## Potential Improvements

1. **Character Comparison Logic**: Replace `s.contains(ca;cb)` with direct equality check - the current approach may incorrectly match substrings
2. **Early Termination**: Exit loop immediately when first difference is found rather than counting all differences
3. **Code Readability**: Add whitespace and break into multiple lines for better maintainability
4. **Memory Efficiency**: Use character-at-index access instead of creating slice substrings for each comparison
5. **Input Validation**: Add error handling for invalid input or I/O failures
6. **Simplified Logic**: The `diff` counter is unnecessary since we only need to know if strings are equal (binary result)

**Suggested Refactor:**
```toke
// Use direct character comparison and early exit
if(a[idx] != b[idx]) { 
    io.println("NOT_EQUAL"); 
    return 0 
}
```