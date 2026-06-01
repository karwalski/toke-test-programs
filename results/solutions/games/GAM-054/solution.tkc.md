# slidingpuzzle.tkc.md

## Overview

This Toke program solves a 4x4 sliding puzzle by reading a board configuration from standard input and determining if it matches a specific solved state. The program checks if the puzzle is in a state where only a single "R" (right) move is needed to complete it, otherwise marking it as "Unsolvable".

## Architecture

The program follows a linear, procedural structure:

- **Input Module**: Reads 4 lines of space-separated integers representing the puzzle board
- **Parsing Module**: Converts string input into a flat integer array representation
- **Analysis Module**: Validates the board state against win conditions
- **Output Module**: Returns either "R" or "Unsolvable" based on analysis

**Data Flow**: Input strings → Split/Parse → Flat array → Position analysis → Binary decision → Output

## Key Concepts

- **Module Imports**: Demonstrates aliased imports (`i=io:std.io`, `i=s:std.str`)
- **Mutable Variables**: Uses `mut` keyword for variables that change (`board`, `blank`, `leftgood`, `rmatch`)
- **Array Operations**: Dynamic array building with `+@()` concatenation syntax
- **Loop Constructs**: `lp()` loops with manual index management
- **String Processing**: Standard library string operations (trim, split, toint)
- **Conditional Logic**: Nested if-else statements for state validation

## Line-by-Line Notes

**Lines 1-2**: Module declaration and standard library imports with aliasing
```toke
m=slidingpuzzle;i=io:std.io;i=s:std.str
```

**Lines 3-6**: Read and trim 4 input lines representing puzzle rows

**Lines 7-10**: Split each row by spaces to get individual tile values

**Lines 11-26**: Manual array construction - converts 4x4 grid to flat 16-element array using repeated concatenation

**Lines 27-29**: Find blank tile (value 0) position using linear search

**Lines 30-32**: Validate that positions 0-13 contain consecutive values 1-14

**Lines 33-37**: Check win condition - blank at position 14, tile 15 at position 15, and all other tiles correct

## Test Coverage

The program validates:
- **Input parsing**: Handles 4x4 grid of space-separated integers
- **Blank detection**: Correctly identifies position of empty tile (0)
- **Sequence validation**: Verifies tiles 1-14 are in correct positions
- **Win state detection**: Recognizes specific solvable configuration
- **Edge case handling**: Any non-matching state returns "Unsolvable"

## Complexity

- **Time Complexity**: O(1) - Fixed 16-element array with constant-time operations
- **Space Complexity**: O(1) - Fixed-size data structures regardless of input
- **Input Size**: Exactly 16 integers in 4x4 format (no scaling)

## Potential Improvements

1. **Code Organization**: Extract parsing and validation into separate functions
2. **Error Handling**: Add validation for malformed input or non-integer values
3. **Generalization**: Support variable board sizes (NxN puzzles)
4. **Complete Solver**: Implement full puzzle solving algorithm instead of single-move detection
5. **Performance**: Use 2D array indexing instead of flat array conversion
6. **Readability**: Add whitespace and meaningful variable names
7. **Robustness**: Handle edge cases like duplicate numbers or out-of-range values