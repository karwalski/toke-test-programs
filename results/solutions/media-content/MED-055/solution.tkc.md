# align.tkc.md

## Overview

This Toke program implements a text alignment utility that reads formatting parameters and text from standard input, then outputs the text aligned according to the specified mode (left, right, center/centre) and width. The program supports left-alignment (default), right-alignment, and center-alignment within a given character width.

## Architecture

The program consists of two main components:
- **`align` function**: Core text alignment logic that handles padding calculations and string manipulation
- **`main` function**: Input/output handler that parses command-line parameters and coordinates the alignment operation

**Data Flow**:
1. Read alignment parameters (mode and width) from first input line
2. Read text to be aligned from second input line  
3. Process text through alignment function
4. Output formatted result

## Key Concepts

- **String manipulation**: Extensive use of `std.str` module for concatenation, length calculation, splitting, and trimming
- **Mutable variables**: Uses `mut` keyword for variables that need to be modified (counters, accumulators)
- **Conditional branching**: Nested `if-el` statements for mode selection
- **Loop constructs**: `lp` (loop) for iterative string building
- **Module aliasing**: Compact aliases (`i`, `s`, `m`) for standard library modules
- **Type annotations**: Explicit typing with `$str`, `$i64` for function parameters and returns

## Line-by-Line Notes

**Module imports & aliases**: `m=align;i=io:std.io;i=s:std.str` - Creates short aliases for the current module and standard library modules

**Padding calculation**: The nested conditionals handle three alignment modes:
- `right`: All padding goes before the text
- `centre`/`center`: Half the padding goes before text (supports both spellings)
- Default (left): No leading padding

**First padding loop**: `lp(idx<pad){result=s.concat(result;" ");idx=idx+1}` - Adds leading spaces for right/center alignment

**Second padding loop**: `lp(s.len(result)<width){result=s.concat(result;" ")}` - Adds trailing spaces to reach target width

**Input parsing**: `s.split(line;" ")` splits the first input line to extract mode and width parameters

## Test Coverage

To thoroughly test this program, verify:
- **Left alignment**: Default behavior with various text lengths
- **Right alignment**: Text positioned at right edge of specified width  
- **Center alignment**: Text centered with equal padding (test both "center" and "centre" spellings)
- **Edge cases**: Text longer than specified width, zero/negative width, empty input
- **Parameter parsing**: Missing parameters, invalid width values, unrecognized modes

## Complexity

- **Time Complexity**: O(w) where w is the target width, due to character-by-character string concatenation in padding loops
- **Space Complexity**: O(w) for the result string storage

## Potential Improvements

1. **Performance**: Replace character-by-character concatenation with bulk string operations or padding functions if available in `std.str`

2. **Input validation**: Add error handling for invalid width values, malformed input, and unsupported alignment modes

3. **Code organization**: Extract padding logic into separate helper functions for better readability and maintainability

4. **Extended functionality**: Support additional alignment modes (justify), custom padding characters, or multiple-line text alignment

5. **Documentation**: Add inline comments and more descriptive variable names for better code comprehension

6. **Robustness**: Handle edge cases like negative widths or text longer than target width more gracefully