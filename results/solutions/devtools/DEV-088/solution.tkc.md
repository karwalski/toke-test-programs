# Schema Parser - Companion Documentation

## Overview

This Toke program parses type definitions from input text and reformats them into a clean schema representation. It reads multiline input containing type declarations with fields, extracts the type names and their field definitions, and outputs them in a structured format with proper indentation.

## Architecture

The program follows a pipeline architecture:

1. **Input Collection Module** - Reads multiline input until two consecutive empty lines
2. **Parsing Engine** - Processes input line-by-line to extract type definitions
3. **Field Processor** - Handles both simple fields and function signatures with parameter lists
4. **Output Formatter** - Reconstructs the schema in reverse order with clean formatting

Data flows through mutable collections (`names` and `bodies` arrays) that accumulate parsed results, with state tracking via `active`, `curname`, and `curbody` variables.

## Key Concepts

- **Mutable Variables**: Extensive use of `mut.` prefix for state management
- **String Manipulation**: Heavy reliance on `std.str` for parsing (split, concat, trim, slice)
- **Array Operations**: Dynamic arrays with `.push()`, `.get()`, and `.len()` methods
- **Control Flow**: Nested loops (`lp`) with conditional branching (`if`/`el`)
- **Module System**: Clean imports with aliases (`i=io:std.io`, `i=s:std.str`)

## Line-by-Line Notes

**Input Collection (first `lp` loop)**: Uses `prevempty` flag to detect double newlines as termination condition. The `got` variable ensures at least one line was read before checking for termination.

**Type Detection**: Looks for "type " prefix, extracts name by splitting on "{" and trimming whitespace.

**Field Processing**: Handles two cases:
- Function signatures: Splits on parentheses to separate name from parameters, then extracts return type after ":"
- Simple fields: Splits on ":" and handles multi-part types by rejoining with colons

**Reverse Output**: Processes collected types in reverse order (`r=cnt-1;r>=0;r=r-1`) to maintain declaration dependencies.

## Test Coverage

To thoroughly test this program, verify:

1. **Basic types** with simple field declarations
2. **Function signatures** with parameter lists and return types  
3. **Multi-part types** (e.g., `std.collections.Map`)
4. **Multiple type definitions** in single input
5. **Empty lines within type definitions**
6. **Malformed input** handling
7. **Single vs double newline termination**

## Complexity

- **Time**: O(n×m) where n = input lines, m = average line length (due to string operations)
- **Space**: O(n) for storing all input lines and parsed results
- **String Operations**: Each concat/split creates new strings, leading to O(k²) behavior for k total characters

## Potential Improvements

1. **Error Handling**: Add validation for malformed type definitions and provide meaningful error messages
2. **Performance**: Use string builder pattern instead of repeated concatenation
3. **Robustness**: Handle edge cases like nested braces, comments, or escaped characters
4. **Formatting**: Add options for different output styles (JSON, YAML, etc.)
5. **Memory**: Stream processing for large inputs instead of loading everything into memory
6. **Parsing**: Implement proper tokenizer/parser instead of string-based heuristics
7. **Testing**: Add comprehensive test suite with edge cases and regression tests