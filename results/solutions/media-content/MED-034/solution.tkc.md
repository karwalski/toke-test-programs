# mdconv.tkc.md

## Overview

This program converts text between two formatting styles: asterisk-based and underscore-based markdown emphasis. It reads a mode selection and input text from stdin, then performs bidirectional conversion between `*` and `_` characters while handling double-character sequences (e.g., `**` ↔ `__`).

## Architecture

The program consists of two main components:
- **`conv` function**: Core conversion logic that processes character-by-character replacement with lookahead for double sequences
- **`main` function**: I/O handler that reads mode and text, delegates to `conv`, and outputs results

Data flows from stdin → mode parsing → text input → conversion → stdout output.

## Key Concepts

**Toke Language Features Demonstrated:**
- **Module system**: Uses aliased imports (`m=mdconv`, `i=io:std.io`, `s:std.str`)
- **Type annotations**: Explicit parameter and return types (`$str`, `$i64`)
- **Mutable variables**: `mut` keyword for `result` and `i` counter
- **String manipulation**: Heavy use of `std.str` module (`len`, `slice`, `concat`)
- **Control flow**: `lp` (loop), `if`/`el` (if/else) constructs
- **Standard I/O**: `readln()`, `println()` from `std.io`

## Line-by-Line Notes

```toke
let dbl=s.concat(fromm;fromm);let tdbl=s.concat(tom;tom)
```
Pre-computes double-character sequences to avoid repeated concatenation in the loop.

```toke
if(i+1<len){let two=s.slice(text;i;i+2);if(two=dbl)
```
Lookahead logic: checks if current position + next character forms a double sequence before processing single characters.

```toke
result=s.concat(result;tdbl);i=i+2
```
When double sequence found, replaces with target double sequence and advances index by 2.

```toke
el{let ch=s.slice(text;i;i+1)
```
Fallback to single-character processing when no double sequence detected.

```toke
let mode=s.trim(io.readln())
```
Reads conversion direction, with `trim()` removing potential whitespace issues.

## Test Coverage

**Recommended test cases should verify:**
- Single character conversion: `*text*` ↔ `_text_`
- Double character conversion: `**bold**` ↔ `__bold__`
- Mixed sequences: `*italic* **bold**` ↔ `_italic_ __bold__`
- Edge cases: Empty strings, text with no target characters
- Both conversion directions: "to-underscore" and reverse mode

## Complexity

- **Time Complexity**: O(n) where n is input text length (single pass with occasional 2-character lookahead)
- **Space Complexity**: O(n) for result string construction (could be optimized with in-place operations if Toke supported them)

## Potential Improvements

1. **Performance**: Replace string concatenation with buffer/array building to reduce O(n²) concatenation overhead
2. **Error Handling**: Add validation for malformed input modes and I/O error handling
3. **Functionality**: Support additional markdown conversions (bold/italic combinations, escaping)
4. **Code Structure**: Extract constants for mode strings, add input validation functions
5. **Memory**: Implement streaming processing for large files instead of loading entire text into memory
6. **Robustness**: Handle edge cases like unmatched emphasis markers or nested formatting