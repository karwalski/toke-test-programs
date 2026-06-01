# craps.tkc.md

## Overview

This program implements a craps game simulator that evaluates dice rolls according to standard craps rules. It reads game state and dice values from input, then determines whether the roll results in a win, loss, continuation, or establishes a point.

## Architecture

The program consists of two main functions:
- **`crapsroll`** — Core game logic function that evaluates dice rolls based on craps rules
- **`main`** — I/O handler that reads input, parses game state, and outputs results

Data flows from standard input through string parsing to the game logic function, with results written to standard output.

## Key Concepts

- **Module imports**: Demonstrates aliased imports (`io:std.io`, `s:std.str`)
- **Function definitions**: Shows parameter typing with `$i64` and return types with `$str`
- **Conditional logic**: Extensive use of `if` statements for game rule implementation
- **String manipulation**: String concatenation, integer conversion, splitting, and trimming
- **Mutable variables**: Uses `mut` keyword for state management
- **Early returns**: Uses `<` operator for function returns

## Line-by-Line Notes

**Import section**: Creates module aliases `m=craps`, `io` for std.io, and `s` for std.str

**`crapsroll` function**:
- Takes three parameters: two dice values and current game state (0 = come-out roll)
- Come-out roll logic (`state=0`): 7,11 win; 2,3,12 lose; others set point
- Point roll logic (`state≠0`): matching point wins; 7 loses; others continue
- Returns descriptive strings for each outcome

**`main` function**:
- Reads and trims first line to determine game state
- Parses "comeout" as state 0, otherwise converts to integer point value
- Splits second line on spaces to extract two dice values
- Calls `crapsroll` and prints result

## Test Coverage

Effective testing should verify:
- Come-out roll scenarios (natural wins 7,11; craps losses 2,3,12; point establishment 4,5,6,8,9,10)
- Point roll scenarios (point hit for win; seven-out for loss; other numbers continue)
- Input parsing (both "comeout" string and numeric point values)
- Edge cases (invalid inputs, boundary values)

## Complexity

- **Time**: O(1) — Fixed number of conditional checks regardless of input
- **Space**: O(1) — Uses constant additional memory for variables and string operations

## Potential Improvements

1. **Error handling**: Add validation for invalid dice values (not 1-6) and malformed input
2. **Code formatting**: Break into multiple lines for better readability
3. **Input validation**: Verify point values are valid (4,5,6,8,9,10)
4. **Documentation**: Add inline comments explaining craps rules
5. **Modularity**: Consider separating parsing logic from game logic
6. **Type safety**: Add bounds checking for array access operations
7. **Return consistency**: Standardize return value format (currently mixed strings)