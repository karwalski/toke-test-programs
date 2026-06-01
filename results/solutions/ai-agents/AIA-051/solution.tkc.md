# extract.tkc.md

## Overview

This toke program reads key-value pairs from standard input and converts them into JSON format. It accepts lines with either colon (`:`) or equals (`=`) separators and outputs a properly formatted JSON object.

## Architecture

**Single Module Structure:**
- **Imports**: Standard library modules for I/O (`std.io`) and string manipulation (`std.str`)
- **Main Function**: Single entry point that handles the complete conversion process
- **Data Flow**: Input lines → Parse separators → Extract key-value pairs → Build JSON string → Output

The program follows a simple linear architecture with a main processing loop that accumulates results into a JSON string.

## Key Concepts

**Toke Language Features Demonstrated:**
- **Module aliasing**: `i=io:std.io` and `i=s:std.str` for namespace management
- **Mutable variables**: Extensive use of `mut` for variables that change during execution
- **String manipulation**: Heavy reliance on stdlib string functions (`indexof`, `slice`, `trim`, `concat`)
- **Conditional logic**: Nested `if` statements for separator precedence handling
- **Loop constructs**: `lp()` for main processing loop
- **Type annotations**: Function return type `$i64`

## Line-by-Line Notes

**Lines 4-6**: Initialize mutable state variables - input line buffer, JSON result string starting with `{`, and item counter.

**Lines 8-12**: Separator detection logic with precedence rules - finds both `:` and `=` positions, then determines which separator to use based on availability and position (equals takes precedence if it appears before colon).

**Lines 13-21**: Key-value extraction and JSON formatting - slices the line at separator position, trims whitespace, and builds JSON key-value syntax with proper comma separation for multiple entries.

**Line 25**: Closes JSON object and outputs the complete result.

## Test Coverage

**Recommended test cases should verify:**
- Mixed separator types (`:` and `=` on different lines)
- Separator precedence (lines containing both `:` and `=`)
- Whitespace handling around keys and values
- Empty input handling
- Lines without valid separators (should be skipped)
- Special characters in keys and values

## Complexity

**Time Complexity**: O(n*m) where n is the number of input lines and m is the average line length (due to string operations)

**Space Complexity**: O(k) where k is the total size of the output JSON string

Note: Multiple string concatenations create intermediate strings, making this less efficient than a buffer-based approach.

## Potential Improvements

1. **JSON Escaping**: Add proper escape handling for quotes, backslashes, and control characters in values
2. **Error Handling**: Implement validation for malformed input and provide error messages
3. **Memory Efficiency**: Use string builder pattern instead of repeated concatenation
4. **Input Validation**: Add checks for duplicate keys and invalid JSON characters
5. **Configuration**: Allow customizable separators and output formatting options
6. **Streaming**: Handle large inputs without loading everything into memory