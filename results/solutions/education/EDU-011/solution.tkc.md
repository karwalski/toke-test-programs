# Vocabulary Quiz Parser - Companion Documentation (.tkc.md)

## Overview

This Toke program implements a simple vocabulary quiz system that parses JSON-formatted word definitions and evaluates user responses. The program reads a JSON line containing vocabulary data, extracts a word and its definition, then prompts the user and scores their answer as correct or incorrect.

## Architecture

The program consists of two main components:

- **`parsejson` function**: A custom JSON parser that extracts quoted strings from a JSON-formatted line
- **`main` function**: The quiz controller that orchestrates input reading, word extraction, user interaction, and scoring

**Data Flow**:
1. Read JSON line containing vocabulary data
2. Parse JSON to extract word and definition
3. Read additional input lines (quiz metadata, test word, user answer)
4. Compare user answer with correct definition
5. Output result and score

**Module Dependencies**:
- `vocab` (vocabulary module)
- `std.io` for input/output operations
- `std.str` for string manipulation

## Key Concepts

**Toke Language Features Demonstrated**:
- **Type System**: Function signatures with `$str`, `@($str)`, and `$i64` types
- **Mutable Variables**: `mut.` prefix for variables that change during execution
- **Array Operations**: Dynamic array with `push()`, `get()`, and `len()` methods
- **Control Flow**: `if/el` conditionals and `lp()` loops
- **String Operations**: Slicing, concatenation, and trimming
- **Standard Library Usage**: IO operations and string utilities

## Line-by-Line Notes

**Lines 4-6**: Initialize mutable state variables for parsing
- `result`: Accumulates extracted strings
- `inquote`: Boolean flag tracking quote state
- `current`: Builds current string being parsed

**Lines 8-9**: Character-by-character parsing using string slicing
- `s.slice(line;idx;idx+1)` extracts single character at position

**Lines 10-20**: Quote state machine
- Toggles `inquote` flag on quote characters
- Accumulates characters only when inside quotes
- Pushes completed strings to result array

**Lines 26-30**: Word extraction with bounds checking
- Assumes JSON format: `[null, "word", null, "definition"]`
- Safely checks array length before accessing elements

**Lines 36-42**: Answer evaluation and scoring
- Uses `s.trim()` to handle whitespace in user input
- Provides binary scoring (100% or 0%)

## Test Coverage

The current implementation handles:
- ✅ Basic JSON string extraction
- ✅ Quote-delimited string parsing
- ✅ Array bounds checking for word extraction
- ✅ Case-sensitive answer comparison
- ✅ Whitespace trimming in user input

**Missing Test Scenarios**:
- Escaped quotes in JSON strings
- Malformed JSON input
- Empty or insufficient input data

## Complexity

**Time Complexity**: O(n) where n is the length of the JSON input line
- Single pass through input string for parsing

**Space Complexity**: O(k) where k is the number of quoted strings in JSON
- Stores extracted strings in result array

## Potential Improvements

1. **Robust JSON Parsing**: Handle escaped quotes (`\"`) and other JSON escape sequences
2. **Error Handling**: Add validation for malformed JSON and insufficient input data
3. **Case-Insensitive Matching**: Use `s.lower()` for more forgiving answer comparison
4. **Flexible Quiz Format**: Support different JSON structures and multiple question types
5. **Enhanced Scoring**: Implement partial credit for close answers or multiple attempts
6. **Input Validation**: Verify expected input format before processing
7. **Modular Design**: Extract quiz logic into separate functions for better testability