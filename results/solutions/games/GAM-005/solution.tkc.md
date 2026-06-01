# Tic-Tac-Toe AI Companion Documentation (.tkc.md)

## Overview

This program implements a tic-tac-toe AI using the minimax algorithm with alpha-beta-like optimization through move ordering. The program reads a 3x3 board state and current player from standard input, then calculates and outputs the optimal move coordinates using game theory principles.

## Architecture

The program is structured as a collection of utility functions supporting a minimax game tree search:

- **Input/Output Layer**: `main()` handles board parsing and result formatting
- **Game Logic Layer**: `winner()`, `full()` provide game state evaluation
- **Board Manipulation**: `setchar()` creates new board states for tree exploration
- **AI Engine**: `minimax()` implements recursive game tree search with evaluation
- **Dependencies**: Uses standard library modules for I/O (`std.io`) and string manipulation (`std.str`)

**Data Flow**: Input → Board parsing → Minimax search → Move evaluation → Coordinate output

## Key Concepts

- **Mutable Variables**: Demonstrates `mut.` syntax for variables that change during computation
- **Array Literals**: Uses `@(...)` syntax for hardcoded winning patterns and move ordering
- **String Slicing**: Leverages `std.str.slice()` for character-level board access
- **Recursive Functions**: Implements classic minimax with proper base cases and recursive calls
- **Loop Constructs**: Uses `lp(init; condition; increment)` for iteration
- **Module System**: Shows module aliasing (`m=minimax`, `i=io:std.io`, `i=s:std.str`)

## Line-by-Line Notes

**Lines 1**: Module aliases setup - note the reuse of identifier `i` for both io and string modules
**Winner function**: Uses hardcoded array of winning line indices (rows, columns, diagonals) rather than computing them
**Move ordering**: `@(4;0;1;2;3;5;6;7;8)` prioritizes center (4) then corners for better pruning efficiency
**Board representation**: Single 9-character string where positions map to `row*3+col`
**Minimax scores**: Uses +10/-10 for terminal wins, 0 for draws
**Input parsing**: Expects 4 lines: 3 board rows + current player ("X" or "O")

## Test Coverage

The implementation should be tested with:

- **Terminal positions**: Board states where X wins, O wins, or draw occurs
- **Early game**: Empty or near-empty boards to verify opening move selection
- **Mid-game**: Complex positions requiring deep search
- **Edge cases**: Full boards, invalid inputs, single-move-to-win scenarios
- **Both players**: Verify correct behavior for both X and O as current player

## Complexity

- **Time Complexity**: O(9!) worst case for empty board, but move ordering improves average case significantly
- **Space Complexity**: O(d) where d is maximum recursion depth (≤9 for tic-tac-toe)
- **Optimization**: Center-first move ordering reduces effective branching factor in practice

## Potential Improvements

1. **Alpha-Beta Pruning**: Add explicit alpha-beta parameters to eliminate redundant subtree exploration
2. **Input Validation**: Add bounds checking and format validation for robustness
3. **Memoization**: Cache previously computed board positions to avoid recalculation
4. **Code Organization**: Extract constants (winning lines, scores) to named variables for clarity
5. **Error Handling**: Add graceful handling for malformed input or impossible board states
6. **Performance**: Consider iterative deepening or transposition tables for larger games
7. **Formatting**: Add board visualization functions for debugging and user feedback