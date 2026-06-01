# Text Classification Service - Toke Program Documentation

## Overview

This Toke program implements a text classification service that categorizes user input into three intent categories: "cancel", "billing", and "support". The program uses a hybrid scoring approach combining keyword-based rules with similarity matching against example phrases to determine the most likely intent from user text.

## Architecture

The program is structured in four main functions with a clear data flow:

- **`scorematch`** — Core similarity function that calculates word overlap between texts
- **`classify`** — Main classification engine using keyword rules and example matching
- **`parseintents`** — JSON parser that extracts text from input and formats output
- **`main`** — Entry point handling I/O operations

**Data Flow:** Input JSON → Text Extraction → Classification → Formatted JSON Output

## Key Concepts

- **Type System**: Demonstrates Toke's type annotations (`$str`, `$f64`, `$i64`, `@($str)` for arrays)
- **Standard Library Usage**: String manipulation (`std.str`) and I/O operations (`std.io`)
- **Mutable Variables**: Uses `mut` keyword for variables that change during computation
- **Control Flow**: Shows loop constructs (`lp`) and conditional logic
- **Function Composition**: Functions call each other to build complex behavior

## Line-by-Line Notes

**Lines 1-3**: Module imports and aliases (`m=classify`, `i=io:std.io`, `i=s:std.str`)

**scorematch function**: 
- Splits both input texts into word arrays using space delimiter
- Double nested loop compares every word from text against every word from pattern
- Returns ratio of matching words to total words in text (0.0 if empty)

**classify function**:
- Initializes three mutable score counters for each intent category
- Applies keyword-based scoring (e.g., "cancel" adds 0.5 to cancel score)
- Enhances scores using similarity matching against provided examples (20% weight)
- Determines best category by highest score and formats as JSON response

**parseintents function**:
- Hardcodes example arrays for each intent category
- Parses JSON input to extract text field using string operations
- Falls back to default "cancel" classification on parse errors

## Test Coverage

The current implementation includes basic example data:
- **Cancel Intent**: "cancel my plan"
- **Billing Intent**: "how much do I owe" 
- **Support Intent**: "app is crashing"

Error handling covers malformed JSON input by defaulting to cancel classification.

## Complexity

- **Time Complexity**: O(n×m×k) where n = input words, m = example phrases, k = words per example
- **Space Complexity**: O(n) for word arrays and temporary string operations
- **Bottleneck**: The nested loops in scorematch function for similarity calculation

## Potential Improvements

1. **Performance**: Replace O(n²) word matching with hash-based lookups
2. **Accuracy**: Implement fuzzy string matching for typos and variations
3. **Maintainability**: Extract hardcoded examples to external configuration
4. **Robustness**: Add comprehensive JSON parsing with proper error handling
5. **Features**: Support confidence thresholds and "unknown" intent category
6. **Scoring**: Use TF-IDF or more sophisticated NLP similarity metrics
7. **Testing**: Add comprehensive test suite with edge cases and validation data