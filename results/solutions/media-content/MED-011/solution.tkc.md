# titletoslug.tkc.md

## Overview

This toke program converts multiple lines of text input into URL-friendly slugs by converting uppercase letters to lowercase, replacing non-alphanumeric characters with hyphens, and removing trailing hyphens. The program reads from standard input line by line and outputs the slugified versions concatenated with newlines.

## Architecture

The program is structured as a single module with four main functions:

- **`lower()`** - Character-level case conversion utility
- **`isalnum()`** - Character classification for alphanumeric detection  
- **`slugify()`** - Core slug transformation logic
- **`main()`** - Input/output handling and program orchestration

**Data Flow:**
```
stdin → main() → slugify() → [lower(), isalnum()] → stdout
```

The program uses the standard library modules `std.io` for I/O operations and `std.str` for string manipulation.

## Key Concepts

**Toke Language Features Demonstrated:**
- **Module system**: Imports with aliases (`i=io:std.io`, `i=s:std.str`)
- **Type annotations**: Explicit parameter and return types (`c:$str):$str`)
- **Mutable variables**: `mut.` prefix for variables that change
- **String operations**: Slicing, concatenation, length calculation
- **Control flow**: `if/el` conditionals and `lp` (loop) constructs
- **Early returns**: `<` operator for function returns

## Line-by-Line Notes

**Character Processing Functions (lines 1-2):**
- `lower()` uses exhaustive if-chain for A-Z → a-z conversion (no built-in case conversion)
- `isalnum()` checks for letters (a-z) and digits (0-9) after normalization

**Slugify Logic (line 3):**
- `lasthyphen` flag prevents consecutive hyphens in output
- Character-by-character processing with index-based string slicing
- Trailing hyphen removal using string slice operation

**Main Function (line 4):**
- `first` flag manages newline insertion between multiple input lines
- Loop continues until empty line encountered (`s.len(line)>0`)
- Accumulates results in `input` string before final output

## Test Coverage

To verify correctness, test cases should cover:

- **Basic conversion**: "Hello World" → "hello-world"  
- **Multiple spaces/punctuation**: "Title!!! With??? Spaces" → "title-with-spaces"
- **Edge cases**: Empty strings, single characters, all punctuation
- **Trailing hyphens**: "Title-" → "title" (hyphen removal)
- **Multi-line input**: Proper newline handling between slugified lines

## Complexity

- **Time Complexity**: O(n*m) where n = number of lines, m = average line length
- **Space Complexity**: O(n*m) for storing accumulated output string
- **Character operations**: O(1) for each `lower()` and `isalnum()` call (constant-time lookups)

## Potential Improvements

1. **Performance**: Replace character-by-character if-chains with lookup tables or built-in case conversion
2. **Memory efficiency**: Stream output instead of accumulating full result string
3. **Unicode support**: Handle non-ASCII characters and international text
4. **Configurability**: Allow custom slug separators or character handling rules
5. **Input validation**: Handle edge cases like extremely long lines or invalid input
6. **Code organization**: Extract character utilities into separate module for reusability