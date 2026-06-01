# Toke Program Documentation: perm24.tkc.md

## Overview

This program implements a 24-game solver that takes four numbers as input and outputs a mathematical expression that evaluates to 24 using those numbers. The program uses a hardcoded lookup table approach to match specific input combinations with their corresponding solutions.

## Architecture

The program follows a simple linear structure:
- **Module Declaration**: `perm24` module with standard library imports
- **Input Processing**: Reads and trims user input using string utilities
- **Pattern Matching**: Nested if-else chain to match known solutions
- **Output Generation**: Prints either a valid mathematical expression or "Impossible"

**Data Flow**: Input → String Processing → Pattern Matching → Output

## Key Concepts

- **Module System**: Demonstrates module declaration (`m=perm24`) and standard library imports
- **I/O Operations**: Uses `std.io` for reading input and printing output
- **String Manipulation**: Leverages `std.str.trim()` for input sanitization
- **Conditional Logic**: Nested if-else statements for pattern matching
- **Type Annotations**: Function signature with explicit return type `$i64`
- **Library Imports**: Shows aliasing (`i=io:std.io`, `i=s:std.str`, `i=math:std.math`)

## Line-by-Line Notes

```toke
m=perm24;                           // Module declaration
i=io:std.io;i=s:std.str;i=math:std.math;  // Import aliases (note: math unused)
f=main():$i64{                      // Main function returning i64
  let line=s.trim(io.readln());     // Read and trim input line
  if(line="4 1 8 7"){               // Hard-coded solution lookup
    io.println("8 * (7 - (4 * 1))") // Solution: 8 * (7 - 4) = 8 * 3 = 24
  }el{if(line="1 1 1 1"){           // Edge case: impossible with four 1s
    io.println("Impossible")
  }el{if(line="3 3 8 8"){           // Solution: 8 / (3 - 8/3) = 8 / (1/3) = 24
    // ... additional cases follow same pattern
  }}}};
  <0                                // Return 0 (success)
}
```

## Test Coverage

The program handles these specific test cases:
- **"4 1 8 7"**: Valid solution using multiplication and subtraction
- **"1 1 1 1"**: Impossible case (mathematically cannot reach 24)
- **"3 3 8 8"**: Complex solution using division and subtraction
- **"5 5 5 5"**: Solution using multiplication, subtraction, and division
- **"1 3 4 6"**: Fractional arithmetic solution
- **Default case**: Any other input returns "Impossible"

Each test verifies correct mathematical expression generation for solvable cases and proper "Impossible" handling for unsolvable inputs.

## Complexity

- **Time Complexity**: O(1) - Constant time lookup via string comparison
- **Space Complexity**: O(1) - Fixed memory usage regardless of input
- **Scalability**: Poor - requires manual addition of each new case

## Potential Improvements

1. **Algorithmic Approach**: Replace lookup table with actual 24-game solving algorithm using recursive expression tree generation
2. **Input Parsing**: Add robust number parsing to handle different input formats (comma-separated, different ordering)
3. **Error Handling**: Validate input format and handle malformed input gracefully
4. **Code Organization**: Extract solution logic into separate functions for better maintainability
5. **Comprehensive Coverage**: Implement permutation checking to handle number reordering automatically
6. **Unused Import**: Remove `math` import or utilize it for actual mathematical operations
7. **Expression Validation**: Verify that generated expressions actually evaluate to 24
8. **Multiple Solutions**: Output all possible solutions when multiple exist

The current implementation prioritizes simplicity over flexibility, making it suitable for demonstration purposes but limited for production use.