# Certificate Parser Program Documentation (.tkc.md)

## Overview

This Toke program parses JSON-like input containing student certification data and outputs a formatted certificate string. The program reads structured data from standard input, extracts student information (name, course, completion date, and score), calculates a letter grade, and generates a standardized certificate output format.

## Architecture

### Modules
- **cert**: Main module container
- **std.io**: Standard I/O operations for reading input and writing output
- **std.str**: String manipulation utilities for parsing and formatting

### Functions
- **`grade(score: $i64): $str`**: Pure function that converts numeric scores to letter grades
- **`main(): $i64`**: Entry point that orchestrates input parsing, data extraction, and output formatting

### Data Flow
1. Read line from standard input
2. Parse JSON-like structure by splitting on commas
3. Extract key-value pairs for student data
4. Convert numeric score to letter grade
5. Format and output certificate string

## Key Concepts

### Toke Language Features Demonstrated
- **Module imports**: Using aliased imports (`i=io:std.io`, `i=s:std.str`)
- **Function definitions**: Type-annotated parameters and return values
- **Mutable variables**: `mut` keyword for changeable state
- **Control flow**: `if` statements and `lp` (loop) constructs
- **String operations**: Extensive use of string manipulation functions
- **Type system**: Explicit typing with `$i64` and `$str`

### Standard Library Usage
- String processing: `slice`, `split`, `trim`, `contains`, `concat`, `len`, `toint`
- I/O operations: `readln`, `println`
- Collection access: `get` method for array-like access

## Line-by-Line Notes

### Grade Function
```toke
f=grade(score:$i64):$str{if(score>=90){<"A"};if(score>=80){<"B"};...}
```
Uses cascading if statements for grade boundaries. Returns immediately on first match due to early return syntax (`<`).

### Input Processing
```toke
let content=s.slice(line;1;s.len(line)-1);
```
Removes surrounding brackets/braces from input by slicing from index 1 to length-1.

### Key-Value Extraction
```toke
if(s.contains(part;"student")){let kv=s.split(part;":");...}
```
Pattern repeated for each field: check if part contains key, split on colon, extract and clean value.

### Score Cleaning
```toke
if(s.contains(cleanval;"}")){let pos=s.len(cleanval)-1;cleanval=s.slice(cleanval;0;pos)}
```
Handles trailing braces that might appear in the score value due to JSON formatting.

### Output Formatting
```toke
let msg1=s.concat("CERTIFICATE | ";student);...
```
Builds final output string through sequential concatenations instead of using a single format operation.

## Test Coverage

To properly test this program, verify:
- **Valid input**: JSON with all required fields (student, course, completion_date, score)
- **Grade boundaries**: Scores at 90, 80, 70, 60 thresholds and edge cases
- **Missing fields**: Behavior when fields are absent or malformed
- **Score parsing**: Integer conversion with various numeric formats
- **String cleaning**: Proper handling of quotes and braces in values

## Complexity

- **Time Complexity**: O(n) where n is the length of input string
  - Single pass through input for splitting
  - Linear search through parts array
  - String operations are generally linear in string length

- **Space Complexity**: O(n) for storing split parts and intermediate string values
  - Multiple string copies created during concatenation

## Potential Improvements

### Code Quality
- **Error handling**: Add validation for missing fields and malformed input
- **String building**: Use a more efficient string building mechanism instead of multiple concatenations
- **Input validation**: Verify score is within expected range (0-100)

### Functionality
- **Flexible parsing**: Support for different input formats beyond comma-separated
- **Configurable grading**: Allow custom grade scales
- **Output templates**: Configurable certificate format strings

### Performance
- **Single-pass parsing**: Combine field extraction into one loop iteration
- **Memory efficiency**: Reduce intermediate string allocations
- **Input streaming**: Handle larger inputs without loading entire content into memory

### Maintainability
- **Constants**: Extract grade thresholds and format strings as named constants
- **Separate parsing logic**: Split parsing and formatting into separate functions
- **Documentation**: Add inline comments for complex parsing logic