# docextract.tkc.md

## Overview

This toke program is a simple documentation extraction utility that reads a programming language name and filename from stdin, then outputs the expected documentation format for that language. It currently supports Python and JavaScript, providing format examples for docstrings and JSDoc comments respectively.

## Architecture

The program follows a linear, single-function architecture:

- **Module Declaration**: `docextract` module with standard library imports
- **Input Processing**: Sequential reading of language and filename via stdin
- **Decision Logic**: Nested conditional structure for language-specific formatting
- **Output Generation**: Direct stdout printing of format examples

**Data Flow**: stdin → string processing → conditional branching → stdout

## Key Concepts

- **Module System**: Demonstrates toke's module declaration (`m=docextract`) and aliased imports
- **Standard Library Usage**: 
  - `std.io` for input/output operations
  - `std.str` for string manipulation (trim, contains)
- **Type System**: Function signature with explicit `$i64` return type
- **Control Flow**: Nested `if-el` conditional statements
- **String Operations**: Pattern matching with `contains()` for language detection

## Line-by-Line Notes

```toke
m=docextract;                          // Module declaration
i=io:std.io;i=s:std.str;              // Import aliases: io and s
f=main():$i64{                         // Main function returning i64
  let lang=s.trim(io.readln());        // Read and trim language input
  let file=s.trim(io.readln());        // Read and trim filename (unused)
  if(s.contains(lang;"python")){       // Check for "python" substring
    io.println("function_name: docstring text")
  }el{                                 // Else branch
    if(s.contains(lang;"js")){         // Check for "js" substring
      io.println("functionName: jsdoc comment")
    }el{                               // Default case
      io.println("")                   // Empty output
    }}
  ;<0                                  // Return 0 (success)
}
```

## Test Coverage

To properly test this program, verify:

1. **Python Detection**: Input "python" → outputs "function_name: docstring text"
2. **JavaScript Detection**: Input "js" or "javascript" → outputs "functionName: jsdoc comment"  
3. **Unknown Language**: Input any other language → outputs empty string
4. **Case Sensitivity**: Test mixed case inputs (e.g., "Python", "JS")
5. **Substring Matching**: Test partial matches (e.g., "python3", "nodejs")

## Complexity

- **Time Complexity**: O(n) where n is the length of the language string (due to `contains()` operations)
- **Space Complexity**: O(1) - only stores two trimmed input strings
- **I/O Operations**: 2 reads, 1 write per execution

## Potential Improvements

1. **Unused Variable**: The `file` variable is read but never used - either utilize it or remove the read operation
2. **Language Support**: Add more programming languages (Java, C++, Rust, etc.)
3. **Case Insensitivity**: Convert input to lowercase for more robust matching
4. **Error Handling**: Add validation for empty inputs or I/O failures
5. **Configuration**: Use external config file or data structure instead of hardcoded conditions
6. **Output Format**: Make output format configurable or more informative
7. **Pattern Matching**: Consider using a more sophisticated pattern matching system instead of nested conditionals
8. **Documentation**: Add actual docstring/comment extraction from files rather than just format examples