# csvfromjson.tkc.md

## Overview

This Toke program converts a JSON array of objects into CSV format. It reads a single line of JSON from standard input, parses the object structure manually, and outputs the equivalent CSV representation with headers derived from the first object's keys.

## Architecture

The program follows a single-function architecture with nested loops:

- **Module imports**: Standard I/O and string manipulation libraries
- **Main function**: Contains all parsing logic in a linear flow
- **Data flow**: JSON string → manual parsing → CSV string construction → output
- **State management**: Uses mutable variables to track parsing progress and accumulate results

## Key Concepts

- **Standard Library Usage**: Demonstrates `std.io` for input/output and `std.str` for string manipulation
- **Mutable Variables**: Extensive use of `mut` keyword for iterative processing
- **Manual Parsing**: Implements JSON parsing without built-in JSON libraries
- **Loop Constructs**: Uses `lp()` (loop) syntax for iteration
- **String Slicing**: Heavy reliance on `s.slice()` for character-by-character processing
- **Conditional Logic**: `if`/`el` (else) statements for control flow

## Line-by-Line Notes

**Imports & Setup**
```toke
m=csvfromjson;i=io:std.io;i=s:std.str;
```
- Module name declaration and aliased imports for cleaner code

**Input Processing**
```toke
let line=s.trim(io.readln());let inner=s.slice(line;1;s.len(line)-1);
```
- Reads input and strips outer array brackets `[...]`

**Object Splitting**
```toke
let objs=s.split(inner;"},{");
```
- Splits JSON array into individual object strings using `},{` delimiter

**Character-Level Cleaning**
```toke
lp(ci<ol){let ch=s.slice(obj;ci;ci+1);if(ch!="{"){if(ch!="}"){cleaned=s.concat(cleaned;ch)}};ci=ci+1};
```
- Removes remaining `{` and `}` characters from object strings

**Key-Value Parsing**
```toke
let pairs=s.split(cleaned;",");...let kv=s.split(pair;":");
```
- Splits object into comma-separated pairs, then separates keys from values

**Quote Removal**
```toke
let cleankey=s.slice(key;1;keylen-1);let cleanval=s.slice(val;1;vallen-1);
```
- Strips quotation marks from both keys and values

**CSV Construction**
```toke
if(oi=0){result=s.concat(s.concat(header;"\n");row)}el{result=s.concat(s.concat(result;"\n");row)};
```
- First object generates header row, subsequent objects append data rows

## Test Coverage

Potential test cases should verify:
- **Single object**: `[{"name":"John","age":"30"}]` → `name,age\nJohn,30`
- **Multiple objects**: Array with 2+ objects of same structure
- **Empty values**: Objects with empty string values
- **Special characters**: Values containing commas, quotes, or spaces
- **Malformed input**: Missing brackets, invalid JSON structure
- **Edge cases**: Empty array `[]`, single field objects

## Complexity

- **Time Complexity**: O(n×m×k) where n=number of objects, m=average object size, k=average key/value length
- **Space Complexity**: O(n×m) for storing intermediate strings and final result
- **Performance Notes**: Heavy string concatenation may cause performance issues with large datasets due to immutable string operations

## Potential Improvements

1. **Error Handling**: Add validation for malformed JSON input and graceful error messages
2. **Memory Efficiency**: Use string builders or buffers instead of repeated concatenation
3. **Parsing Robustness**: Handle escaped quotes, nested objects, and array values properly
4. **Code Structure**: Break into smaller functions for readability and testability
5. **Edge Case Handling**: Support for empty arrays, null values, and inconsistent object schemas
6. **Performance**: Implement single-pass parsing instead of multiple string operations
7. **Standards Compliance**: Ensure CSV output follows RFC 4180 (proper escaping, quoting rules)
8. **Flexibility**: Add command-line options for custom delimiters or output formatting