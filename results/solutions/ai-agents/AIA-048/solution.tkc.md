# extract.tkc.md

## Overview

This Toke program implements a simple knowledge graph generator that outputs structured relationship data in JSON format. Based on user input, it returns either workplace management relationships (Alice-Bob hierarchy) or company information facts (SpaceX details).

## Architecture

The program follows a linear, single-function architecture:

```
main() → input reading → conditional logic → JSON output
```

**Modules:**
- `extract` (main module)
- `std.io` (I/O operations)
- `std.str` (string manipulation)

**Data Flow:**
1. Read user input via stdin
2. Check for "Alice" keyword in input
3. Output corresponding predefined JSON relationship array
4. Return success code

## Key Concepts

**Toke Language Features Demonstrated:**
- **Module Import System**: Multiple import patterns (`m=extract`, `i=io:std.io`, `i=s:std.str`)
- **Function Definition**: `f=main():$i64` syntax with explicit return type
- **Standard Library Usage**: I/O and string manipulation functions
- **Conditional Logic**: `if-el` branching structure
- **String Methods**: `s.contains()` for pattern matching
- **Return Values**: Implicit return with `<0`

## Line-by-Line Notes

```toke
m=extract;                    // Module declaration
i=io:std.io;                 // Import std.io, alias as 'io'
i=s:std.str;                 // Import std.str, alias as 's'
f=main():$i64{               // Main function returning 64-bit integer
    let input=io.readln();   // Read line from stdin, store in immutable variable
    if(s.contains(input;"Alice")){  // Check if input contains "Alice" substring
        io.println("[{...}]") // Output Alice-Bob management relationships
    }el{                     // Else clause (Toke's abbreviated 'else')
        io.println("[{...}]") // Output SpaceX company facts
    };                       // End conditional block
    <0                       // Return 0 (success) - Toke's return syntax
}
```

## Test Coverage

**Recommended Test Cases:**
- **Positive Match**: Input containing "Alice" → Should output Alice-Bob relationships
- **Negative Match**: Input without "Alice" → Should output SpaceX facts  
- **Edge Cases**: Empty input, "Alice" substring variations, case sensitivity
- **Return Value**: Verify function returns 0 for all valid inputs

**Current Verification:**
- Basic conditional branching logic
- JSON output formatting
- Standard library integration

## Complexity

**Time Complexity:** O(n) where n = input string length (due to `contains()` operation)

**Space Complexity:** O(1) - fixed-size JSON strings, single input variable

**I/O Complexity:** 1 read operation, 1 write operation per execution

## Potential Improvements

1. **Input Validation**: Add error handling for invalid/null input
2. **Case Insensitivity**: Use `s.to_lower()` before contains check
3. **Configuration**: Extract JSON templates to constants or external files
4. **Extensibility**: Replace hardcoded logic with pattern-to-response mapping
5. **Error Handling**: Add proper error codes for different failure modes
6. **JSON Validation**: Ensure output is well-formed JSON
7. **Logging**: Add debug output for input processing steps
8. **Performance**: Consider regex matching for more complex pattern detection

**Refactoring Opportunities:**
- Separate JSON data from logic
- Create reusable relationship generation functions
- Implement configuration-driven response system