# urlenc.tkc.md

## Overview

This Toke program implements a basic URL encoding/decoding utility that handles space characters. It reads a mode ("encode" or "decode") and input text from standard input, then outputs the appropriately transformed text where spaces are converted to/from "%20" sequences.

## Architecture

The program is structured as a single module with three main functions:

```
urlenc module
├── encode(p0: $str): $str     - Converts spaces to "%20"
├── decode(p0: $str): $str     - Converts "%20" back to spaces  
└── main(): $i64               - Entry point handling I/O and mode selection
```

**Data Flow:**
1. `main()` reads mode and text from stdin
2. Calls appropriate transformation function (`encode` or `decode`)
3. Outputs result to stdout

## Key Concepts

- **Module System**: Demonstrates module declaration (`m=urlenc`) and standard library imports
- **String Manipulation**: Extensive use of `std.str` functions (`len`, `slice`, `concat`, `trim`)
- **Mutable Variables**: Uses `mut` keyword for variables that change during iteration
- **Manual Loop Control**: Implements character-by-character processing with explicit index management
- **Conditional Logic**: Simple if-else branching for mode selection and character processing

## Line-by-Line Notes

**Imports & Module:**
```toke
m=urlenc;i=io:std.io;i=s:std.str;
```
- Declares module and creates convenient aliases for I/O and string standard libraries

**Encode Function:**
```toke
lp(let idx=0;idx<n;idx=idx+1){let ch=s.slice(p0;idx;idx+1);...}
```
- Manual loop with index tracking (no for-each construct used)
- `s.slice(p0;idx;idx+1)` extracts single character at position

**Decode Function:**
```toke
if(ch="%"){result=s.concat(result;" ");idx=idx+3}
```
- Assumes "%20" sequence, advances index by 3 to skip entire encoded sequence
- No validation that "20" follows the "%"

**Main Function:**
```toke
let mode=s.trim(io.readln());let text=s.trim(io.readln());
```
- Uses `trim()` to clean input, suggesting awareness of whitespace issues

## Test Coverage

The program would benefit from testing:

- **Encode Cases**: Strings with no spaces, multiple spaces, leading/trailing spaces
- **Decode Cases**: Strings with no encoded sequences, multiple "%20" sequences
- **Edge Cases**: Empty strings, strings with "%" not followed by "20"
- **Mode Validation**: Invalid mode inputs, case sensitivity

## Complexity

- **Time Complexity**: O(n) where n is input string length
- **Space Complexity**: O(n) for result string construction
- **Note**: String concatenation in loop may result in O(n²) behavior if strings are immutable and copied each iteration

## Potential Improvements

1. **Complete URL Encoding**: Handle full character set (alphanumeric + safe chars), not just spaces
2. **Error Handling**: Validate mode input and malformed encoded sequences
3. **Performance**: Use string builder pattern if available to avoid O(n²) concatenation
4. **Robustness**: Validate that "%" is followed by valid hex digits
5. **Code Organization**: Extract character processing logic into helper functions
6. **Input Validation**: Handle EOF conditions and invalid input gracefully
7. **Extended Functionality**: Support encoding/decoding from files or command-line arguments