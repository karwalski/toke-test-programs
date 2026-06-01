# Titlecase Program Documentation (.tkc.md)

## Overview

This toke program implements title case formatting for text input. It reads a line of text from standard input and converts it to proper title case, where the first word and all major words are capitalized while minor words (articles, prepositions, conjunctions) remain lowercase unless they appear at the beginning.

## Architecture

The program is structured as a single module with four main functions:

- **`isminor()`** - Determines if a word should remain lowercase in title case
- **`toupper()`** - Manual character-to-uppercase conversion mapping
- **`cap()`** - Capitalizes the first letter of a word using the toupper function
- **`main()`** - Orchestrates the title case conversion process

**Data flow:** Input line → word splitting → per-word case logic → result concatenation → output

## Key Concepts

- **Type System**: Demonstrates explicit type annotations (`$str`, `$bool`, `$i64`)
- **Standard Library Usage**: 
  - `std.io` for input/output operations
  - `std.str` for string manipulation (split, slice, concat, contains, len)
- **Mutable Variables**: Uses `mut.` prefix for variables that change during execution
- **Control Flow**: Nested conditionals and loop construct (`lp`)
- **Function Definitions**: Multiple function definitions with typed parameters and return values

## Line-by-Line Notes

**Lines 1-2**: Module declaration and library imports using aliasing (`i=io`, `i=s`)

**`isminor()` function**: Checks word length alongside content to precisely identify minor words (avoids false positives with words containing minor words as substrings)

**`toupper()` function**: Manual uppercase mapping for all 26 lowercase letters using sequential if statements (likely due to absence of built-in case conversion)

**`cap()` function**: 
- Handles edge case of empty strings
- Uses string slicing to separate first character from remainder
- Note: `s.format(first;"%s")` appears redundant

**`main()` function**:
- Uses mutable variables for building result string and loop counter
- Applies special logic: first word always capitalized, subsequent words follow minor/major word rules
- Manual space insertion between words during concatenation

## Test Coverage

The program should be tested with:
- **Basic cases**: Simple sentences with common minor words
- **Edge cases**: Single words, empty input, words at boundaries
- **Minor words**: Verify "a", "of", "the", "to", "and" handling
- **Mixed content**: Sentences with both minor and major words
- **Position sensitivity**: Minor words at start vs. middle of sentences

Example test cases:
```
Input: "the quick brown fox"
Expected: "The Quick Brown Fox"

Input: "a tale of two cities"
Expected: "A Tale of Two Cities"
```

## Complexity

- **Time Complexity**: O(n×m) where n is the number of words and m is average word length
- **Space Complexity**: O(n) for storing word array and building result string
- **Character conversion**: O(1) lookup per character (though implemented as O(26) linear search)

## Potential Improvements

1. **Performance**: Replace linear character search in `toupper()` with hash map or built-in case conversion
2. **Completeness**: Expand minor words list (in, on, at, by, for, with, etc.)
3. **Robustness**: Handle punctuation attached to words, multiple spaces, special characters
4. **Code Quality**: Remove redundant `s.format()` call in `cap()` function
5. **Configurability**: Make minor words list configurable rather than hardcoded
6. **Unicode Support**: Handle accented characters and non-ASCII text
7. **Standards Compliance**: Implement full title case rules (e.g., capitalize after colons/hyphens)