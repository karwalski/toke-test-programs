# phone.tkc.md

## Overview

This Toke program processes phone numbers from standard input, extracting and formatting international phone numbers. It validates that phone numbers contain a country code (indicated by a "+" prefix) and strips all non-digit characters except the plus sign, outputting either a clean formatted number or an error message.

## Architecture

The program follows a functional pipeline architecture with three main components:

- **Input Layer**: `main()` function handles stdin reading loop
- **Processing Layer**: `process()` function orchestrates validation and formatting
- **Utility Layer**: `stripdigits()` function performs character filtering

**Data Flow**: Raw input → Trim whitespace → Validate country code → Extract digits → Format output

## Key Concepts

- **Module System**: Demonstrates Toke's module aliasing (`i=io:std.io`, `i=s:std.str`)
- **Type System**: Explicit type annotations (`$str`, `$i64`) and string mutability (`mut.""`)
- **Standard Library**: Extensive use of `std.str` utilities (trim, contains, slice, concat, len)
- **Control Flow**: C-style for loop (`lp`) with manual index management
- **Function Definitions**: Multi-parameter functions with return type specifications

## Line-by-Line Notes

**Module Imports & Aliases**:
```toke
m=phone;i=io:std.io;i=s:std.str
```
- Creates module `phone` and aliases I/O and string libraries

**`stripdigits()` Implementation**:
```toke
let r=mut."";let n=s.len(line);lp(let idx=0;idx<n;idx=idx+1)
```
- Uses mutable string accumulator and manual string iteration
- Character extraction via `s.slice(line;idx;idx+1)` (single-character slice)
- Digit validation using `s.contains("0123456789";c)`

**`process()` Logic**:
```toke
if(s.contains(t;"+")){let digits=stripdigits(t);<s.concat("+";digits)}
```
- Validates country code presence before processing
- Returns early with error message for invalid format

**Main Loop**:
```toke
lp(line=io.readln();s.len(line)>0;line=io.readln())
```
- Continues until empty line (EOF simulation)
- Note: `io.readln()` called twice per iteration (condition + increment)

## Test Coverage

Recommended test cases should verify:

- **Valid International Numbers**: `+1-234-567-8900` → `+12345678900`
- **Local Numbers**: `234-567-8900` → `INVALID (no country code)`
- **Mixed Characters**: `+33 (0)1 42 34 56 78` → `+33142345678`
- **Edge Cases**: Empty input, whitespace-only, non-numeric content
- **Multiple Country Codes**: Various international prefixes

## Complexity

- **Time**: O(n) per phone number, where n = string length (single pass for trimming + single pass for digit extraction)
- **Space**: O(n) for digit accumulation in worst case (all-digit input)
- **Overall**: O(m×n) for m phone numbers of average length n

## Potential Improvements

1. **Performance**: Replace character-by-character slicing with iterator-based approach
2. **Validation**: Add phone number length validation and country code verification
3. **Error Handling**: Provide more specific error messages for different failure modes
4. **Code Structure**: Extract validation logic into separate function for better modularity
5. **I/O Efficiency**: Eliminate redundant `readln()` calls in loop condition
6. **Regex Support**: Use pattern matching if available in Toke standard library for cleaner digit extraction