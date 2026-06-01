# pathconv.tkc.md

## Overview

This toke program provides path conversion utilities between Unix and Windows file path formats. It reads a target format and a file path from standard input, then converts and outputs the path in the requested format.

## Architecture

The program is structured as a single module `pathconv` with three main functions:

- **`tounix()`** — Converts Windows-style paths to Unix format
- **`towindows()`** — Converts Unix-style paths to Windows format  
- **`main()`** — Handles I/O and orchestrates the conversion process

**Data Flow:**
1. Read conversion type ("unix" or other) from stdin
2. Read source path from stdin
3. Apply appropriate conversion function
4. Output converted path to stdout

## Key Concepts

- **Module System**: Demonstrates toke's module imports (`std.io`, `std.str`)
- **String Manipulation**: Heavy use of string slicing, concatenation, and length operations
- **Mutable Variables**: Uses `mut` keyword for variables that change during iteration
- **Loop Constructs**: Implements `lp` (loop) with manual index management
- **Conditional Logic**: Uses `if`/`el` (else) statements for character-by-character processing
- **Function Return**: Uses `<expression>` syntax for function returns

## Line-by-Line Notes

**Imports & Setup:**
```toke
m=pathconv;i=io:std.io;i=s:std.str;
```
- Declares module name and imports I/O and string standard libraries with aliases

**`tounix()` Function:**
```toke
let start=mut.0;if(s.len(p)>=2){let c0=s.slice(p;0;1);let c1=s.slice(p;1;2);if(c1=":"){start=2}}
```
- Detects Windows drive letters (e.g., "C:") and skips them during conversion
- Sets starting index to 2 if drive letter is found

**Character Processing Loop:**
```toke
lp(let idx=start;idx<s.len(p);idx=idx+1){let ch=s.slice(p;idx;idx+1);if(ch="\\"){result=s.concat(result;"/")}el{result=s.concat(result;ch)}}
```
- Iterates through each character, replacing backslashes with forward slashes

**`towindows()` Function:**
```toke
let result=mut."C:";
```
- Hardcodes "C:" drive prefix for all converted Windows paths

## Test Coverage

The program should be tested with:

- **Unix to Windows**: `/home/user/file.txt` → `C:\home\user\file.txt`
- **Windows to Unix**: `C:\Users\user\file.txt` → `/Users/user/file.txt`  
- **Edge Cases**: Empty paths, paths without drive letters, mixed separators
- **Input Validation**: Non-"unix" target types default to Windows conversion

## Complexity

- **Time Complexity**: O(n) where n is the length of the input path
- **Space Complexity**: O(n) for the result string construction
- **String Operations**: Each character requires a slice and concatenation operation

## Potential Improvements

1. **Input Validation**: Add error handling for malformed paths or invalid conversion types
2. **Drive Letter Flexibility**: Support different drive letters instead of hardcoding "C:"
3. **Path Normalization**: Handle relative paths, double slashes, and `./`/`../` components
4. **Performance**: Use a string builder pattern to reduce concatenation overhead
5. **Cross-Platform Features**: Detect and preserve file permissions, handle case sensitivity
6. **Error Reporting**: Return error codes for invalid operations instead of silent failures
7. **Extended Format Support**: Support UNC paths, network drives, and other platform-specific formats