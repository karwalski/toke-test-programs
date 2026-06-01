# absence.tkc.md

## Overview

This Toke program parses a single line of input (likely JSON) to count different types of absence reasons. It searches for "sick", "family", and "trip" reasons within the input text and reports the count for each category along with a total count.

## Architecture

The program follows a simple linear structure:
- **Input Phase**: Reads a single line from standard input
- **Processing Phase**: Uses a character-by-character scanning loop to find reason patterns
- **Output Phase**: Conditionally prints counts for each absence type and always prints the total

**Data Flow**: Input string → Pattern matching loop → Counters → Formatted output

## Key Concepts

- **Module System**: Demonstrates import aliasing with `io:std.io` and `s:std.str`
- **Mutable Variables**: Uses `mut` keyword for all counter variables
- **String Operations**: Leverages `s.slice()`, `s.len()`, `s.concat()`, and `s.fromint()`
- **Control Flow**: Simple `lp()` loop with nested conditionals
- **Type System**: Function returns `$i64`, uses integer arithmetic

## Line-by-Line Notes

```toke
m=absence;i=io:std.io;i=s:std.str;
```
Module declaration and import aliases for I/O and string operations.

```toke
let sickcount=mut.0;let familycount=mut.0;let tripcount=mut.0;let total=mut.0;let pos=mut.0;
```
Initialize all mutable counters and position tracker to zero.

```toke
lp(pos<s.len(line)){...pos=pos+1};
```
Main scanning loop iterates through each character position in the input line.

```toke
if(pos+14<=s.len(line)){if(s.slice(line;pos;pos+14)="reason\":\"sick\""){...}}
```
Bounds checking before string slicing prevents runtime errors. The magic numbers (14, 16) correspond to the exact lengths of the JSON patterns being matched.

```toke
if(sickcount>0){io.println(...)};
```
Conditional output only prints categories that have non-zero counts.

## Test Coverage

The program should be tested with:
- **Empty input**: Verify zero counts
- **Single reason types**: JSON with only sick/family/trip reasons
- **Mixed reasons**: Multiple different absence types
- **Edge cases**: Malformed JSON, overlapping patterns, boundary conditions
- **Large input**: Performance with lengthy input strings

## Complexity

- **Time Complexity**: O(n×m) where n is input length and m is average pattern length (~15 chars)
- **Space Complexity**: O(1) excluding input storage
- **Performance Issue**: The sliding window approach rescans overlapping substrings inefficiently

## Potential Improvements

1. **JSON Parsing**: Use proper JSON parser instead of string searching for robustness
2. **Algorithm Efficiency**: Implement Boyer-Moore or similar string matching for O(n) performance
3. **Code Organization**: Extract pattern matching into separate functions for readability
4. **Error Handling**: Add input validation and error recovery mechanisms
5. **Configurability**: Make absence types configurable rather than hardcoded
6. **Output Formatting**: Add consistent formatting and potentially support different output formats
7. **Memory Optimization**: Stream processing for very large inputs instead of loading entire line