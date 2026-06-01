# Token Transfer System Documentation (.tkc.md)

## Overview
This Toke program implements a simple token transfer system that tracks balances between two accounts (Alice and Bob). It parses initial balances from JSON input, processes a series of transfer commands, validates transactions for sufficient funds, and outputs either an error message or the final account balances in JSON format.

## Architecture
The program consists of two main components:
- **`parsebal` function**: A JSON parser that extracts balance values for specified account names
- **`main` function**: The core transaction processor that handles initial state setup, transaction validation, and output formatting

Data flows from JSON input → balance initialization → transaction processing loop → final state output.

## Key Concepts
- **String manipulation**: Extensive use of `std.str` for parsing, splitting, and concatenation
- **Mutable variables**: Heavy reliance on `mut` for state tracking (balances, loop counters, flags)
- **Manual JSON parsing**: Custom character-by-character parsing instead of built-in JSON libraries
- **Input/output**: Standard I/O operations for reading transaction data and printing results
- **Type system**: Demonstrates `$str` and `$i64` type annotations
- **Control flow**: Nested loops (`lp`) and conditional logic (`if`/`el`)

## Line-by-Line Notes

**Lines 4-5**: Module imports with aliases (`i=io:std.io`, `i=s:std.str`) - note the duplicate `i=` alias which overwrites the io import.

**Lines 11-23**: Character filtering loop that removes JSON delimiters (`{`, `}`, `"`) to clean keys.

**Lines 24-35**: Similar cleaning process for values, removing braces but preserving other characters.

**Lines 46-50**: Transaction parsing expects format: `<command> <from> <to> <amount>` with minimum 4 parts.

**Lines 51-53**: Balance lookup logic assumes only two accounts (alice/bob).

**Lines 54-57**: Insufficient funds check with error message generation.

**Lines 67-72**: Manual JSON output construction using string concatenation.

## Test Coverage
The program should be tested with:
- **Valid JSON input** with alice/bob balances
- **Successful transfers** within balance limits
- **Insufficient funds scenarios** to verify error handling
- **Edge cases**: malformed JSON, invalid transaction formats, empty input
- **Boundary conditions**: zero balances, exact balance transfers

## Complexity
- **Time Complexity**: O(n×m) where n is the number of transactions and m is the average length of JSON strings (due to character-by-character parsing)
- **Space Complexity**: O(m) for string operations and temporary variables during parsing

## Potential Improvements

1. **JSON Library**: Replace manual parsing with proper JSON library for reliability and performance
2. **Error Handling**: Add comprehensive validation for malformed input and edge cases
3. **Scalability**: Support for more than two accounts using a map/dictionary structure
4. **Code Organization**: Extract transaction validation and balance updates into separate functions
5. **Input Validation**: Verify transaction format and handle negative amounts
6. **Performance**: Reduce string concatenations in parsing loops
7. **Import Fix**: Resolve the duplicate alias issue that overwrites the `io` import
8. **Type Safety**: Add more explicit type checking for parsed numeric values