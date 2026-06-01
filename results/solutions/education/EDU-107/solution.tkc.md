# toke-json-parser.tkc.md

## Overview

This toke program parses a JSON-like input containing student data, prompts, and seed values, then organizes students into pairs and determines a sharing order. The program extracts student names from the input, groups them into pairs (with potential solo participants), and outputs the pairing results along with a presentation order.

## Architecture

```
main() 
└── parsejson(input)
    ├── JSON parsing via string splitting on quotes
    ├── Student extraction and collection
    ├── Prompt and seed value parsing
    ├── Pair formation logic
    └── Output formatting and display
```

**Data Flow:**
1. Read input from stdin
2. Split input on quote characters to tokenize JSON-like structure
3. Extract students, prompt, and seed through sequential parsing
4. Group students into pairs with remainder handling
5. Format and output results with sharing order

## Key Concepts

- **Mutable Variables**: Extensive use of `mut` keyword for stateful computation
- **String Manipulation**: Heavy reliance on `std.str` module for parsing and formatting
- **Array Operations**: Dynamic array building with `push()` and indexed access
- **Control Flow**: Nested loops (`lp`) with conditional branching
- **Type System**: Function signatures with explicit parameter and return types (`$str`, `$void`, `$i64`)
- **Module Imports**: Standard library usage (`std.io`, `std.str`)

## Line-by-Line Notes

**Line Structure**: The entire program is written as a single line with semicolon separators.

**JSON Parsing Strategy**: Uses `s.split(input;"\"")` to tokenize on quotes rather than proper JSON parsing - assumes specific JSON structure.

**Student Extraction**: Searches for "students" keyword, then collects non-empty, trimmed strings until "prompt" is found, filtering out bracket characters.

**Numeric Parsing**: Custom digit extraction for seed values - manually filters characters to build numeric string before conversion.

**Pairing Logic**: Sequential pairing (students 0&1, 2&3, etc.) with remainder students marked as "solo".

**Share Order**: Reverses first two pairs for presentation order (`pairs.get(1), pairs.get(0)`).

## Test Coverage

The program should be tested with:

- **Valid JSON**: Standard student/prompt/seed structure
- **Edge Cases**: Odd number of students, empty student lists, missing fields
- **Malformed Input**: Invalid JSON, missing quotes, non-numeric seeds
- **Boundary Conditions**: Single student, no students, very long student names
- **Input Variations**: Different field ordering, extra whitespace, special characters

## Complexity

**Time Complexity**: O(n²) where n is input length due to nested string operations and repeated concatenations.

**Space Complexity**: O(m) where m is the number of students, storing arrays for students and pairs.

**Performance Bottlenecks**: String concatenation in loops, repeated `s.contains()` calls, and character-by-character processing.

## Potential Improvements

1. **Proper JSON Parser**: Replace string splitting with robust JSON parsing library
2. **Error Handling**: Add validation for malformed input and missing required fields
3. **Code Organization**: Split into smaller, focused functions with clear responsibilities
4. **Performance**: Use string builders instead of repeated concatenation
5. **Randomization**: Utilize the extracted seed value for actual random pairing
6. **Input Validation**: Verify student names are valid and handle duplicate entries
7. **Configuration**: Make pairing strategy configurable (sequential vs. random)
8. **Output Format**: Add options for different output formats (JSON, CSV, etc.)
9. **Memory Efficiency**: Stream processing for large inputs instead of loading everything into memory
10. **Code Readability**: Format code across multiple lines with proper indentation