# snap.tkc.md

## Overview

This Toke program implements a card matching game called "Snap" where two players reveal cards simultaneously. The program reads two lines of space-separated card names, compares them position by position, and declares "Snap!" whenever matching cards are found at the same position.

## Architecture

The program consists of two main components:
- **`streq` function**: A custom string equality checker that wraps strings with delimiters
- **`main` function**: The game logic that processes input, compares cards, tracks matches, and outputs results

**Data Flow**:
1. Read two lines of input (card sequences for each player)
2. Split each line into individual cards
3. Iterate through positions, comparing cards at each turn
4. Track matches ("snaps") and total turns
5. Output final game results

## Key Concepts

**Toke Language Features Demonstrated**:
- **Module imports**: `std.io` for I/O operations, `std.str` for string manipulation
- **Function definitions**: Custom functions with typed parameters and return values
- **Mutable variables**: `mut` keyword for variables that change during execution
- **Control flow**: `if`/`el` conditionals and `lp` (loop) constructs
- **Type system**: Explicit type annotations (`$str`, `$bool`, `$i64`)
- **Standard library usage**: String operations, I/O functions

## Line-by-Line Notes

- **Module imports**: `m=snap; i=io:std.io; i=s:std.str` - Sets up aliases for standard library modules
- **`streq` function**: Uses delimiter wrapping (`"|card|"`) to ensure exact string matching and prevent substring false positives
- **Input processing**: `s.trim()` removes whitespace, `s.split()` creates card arrays
- **Loop structure**: `lp(idx<n)` iterates through card positions, comparing `p1.get(idx)` vs `p2.get(idx)`
- **Snap detection**: Prints turn number when cards match, increments snap counter
- **Score calculation**: `score1` tracks total turns played
- **Output logic**: Different messages for no snaps vs. Player 1 victory

## Test Coverage

Ideal test cases should verify:
- **Exact matches**: Cards with identical names trigger snaps
- **No matches**: Complete sequences without any matching pairs
- **Partial matches**: Some snaps occur, but not every turn
- **Edge cases**: Empty input, single cards, different sequence lengths
- **Whitespace handling**: Extra spaces around card names are properly trimmed

## Complexity

- **Time Complexity**: O(n × m) where n is the number of card positions and m is the average card name length (due to string operations)
- **Space Complexity**: O(n × m) for storing the split card arrays and string manipulations

## Potential Improvements

1. **Error handling**: Add validation for mismatched input lengths or malformed data
2. **Performance**: Replace delimiter-based string comparison with direct equality checks
3. **Code clarity**: Break the dense one-liner into multiple readable statements
4. **Game logic**: Implement proper Snap rules where the first player to call "Snap" wins the round
5. **Input flexibility**: Support different delimiters or card formats
6. **Score tracking**: Add more sophisticated scoring that accounts for reaction time or multiple rounds