# Language Detection Program Documentation (`langdetect.tkc.md`)

## Overview

This Toke program implements a basic language detection system that analyzes input text and identifies whether it's primarily French, English, or Spanish. The program uses keyword matching to determine the most likely language and returns a JSON-formatted confidence score with primary and secondary language predictions.

## Architecture

The program consists of two main modules:
- **Input/Output Module**: Handles reading user input and displaying results
- **Detection Engine**: Core language analysis functionality

**Data Flow**:
1. Text input → Word tokenization → Keyword matching → Scoring → JSON output

**Functions**:
- `detectlang(text: $str): $str` - Main detection algorithm
- `main(): $i64` - Entry point handling I/O

## Key Concepts

**Toke Language Features Demonstrated**:
- **Module imports**: Standard library usage (`std.io`, `std.str`)
- **Mutable variables**: `mut` keyword for counters and result building
- **Loop constructs**: `lp` for iteration over word arrays
- **String manipulation**: Extensive use of string operations (split, trim, replace, concat)
- **Conditional logic**: Nested `if` statements for decision trees
- **Type system**: Explicit type annotations (`$str`, `$i64`)
- **Return syntax**: `<` operator for function returns

## Line-by-Line Notes

**Lines 1-3**: Module imports with aliases (`m`, `i`, `s`) for cleaner code
**Lines 6-9**: Counter initialization for each supported language (French, English, Spanish)
**Lines 11-18**: Text preprocessing - tokenization and punctuation removal
**Lines 20-31**: Keyword matching arrays for each language using hardcoded vocabulary
**Lines 33-35**: Early return for undetectable text cases
**Lines 37-56**: Confidence scoring logic with nested conditionals for primary language selection
**Lines 58-69**: Special case handling for multilingual text detection
**Lines 71-78**: Manual JSON string construction using concatenation
**Lines 81-85**: Main function implementing simple CLI interface

## Test Coverage

The program should be tested with:
- **Pure language samples** - Text containing only French/English/Spanish keywords
- **Mixed language input** - Text with multiple language indicators
- **Unknown language text** - Input with no recognizable keywords
- **Edge cases** - Empty strings, punctuation-only text, single words
- **Confidence thresholds** - Verify 0.98 for clear matches, 0.5 for ambiguous cases

## Complexity

**Time Complexity**: O(n×m) where n = number of words, m = average word length (due to string operations)
**Space Complexity**: O(n) for storing word array and intermediate string operations

The keyword matching is O(1) per word due to fixed vocabulary size.

## Potential Improvements

1. **Vocabulary Expansion**: Replace hardcoded keywords with external dictionary files
2. **Performance**: Use hash maps/sets instead of linear string comparisons
3. **Algorithm Enhancement**: Implement statistical language models or n-gram analysis
4. **JSON Handling**: Use proper JSON library instead of manual string concatenation
5. **Configuration**: Make supported languages and confidence thresholds configurable
6. **Error Handling**: Add validation for malformed input and edge cases
7. **Logging**: Include debug information for detection decision process
8. **Unicode Support**: Handle accented characters and non-ASCII text properly
9. **Streaming**: Support for large text processing without loading everything into memory
10. **Testing Framework**: Add comprehensive unit tests and benchmarking