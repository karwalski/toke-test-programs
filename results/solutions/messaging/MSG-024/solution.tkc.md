# removeduplicates.tkc.md

## Overview

This Toke program processes JSON-like object data to remove duplicate entries based on ID values. It reads a line of input containing comma-separated JSON objects, extracts ID fields, identifies duplicates, and outputs the deduplicated objects along with a count of removed items.

## Architecture

The program follows a single-function design with inline processing:

- **Input Layer**: Reads line input via `std.io.readln()`
- **Parsing Layer**: Splits input by `"},")` delimiter to separate objects
- **Processing Core**: Extracts IDs using string manipulation and maintains duplicate tracking
- **Output Layer**: Reconstructs deduplicated JSON and prints results

Data flows linearly through: input → split → ID extraction → deduplication → reconstruction → output.

## Key Concepts

**Toke Language Features Demonstrated:**
- **Module System**: Uses `std.io` and `std.str` standard library modules
- **Mutable Variables**: Extensive use of `mut` for stateful operations
- **Dynamic Arrays**: Uses `@()` syntax for growable collections
- **Loop Constructs**: `lp()` loops with manual iteration
- **String Operations**: Split, concatenation, and conversion functions
- **Type System**: Explicit `$i64` return type annotation

## Line-by-Line Notes

```toke
m=removeduplicates;i=io:std.io;i=s:std.str;
```
Module declarations with aliasing (`io` and `s` for brevity).

```toke
let objs=s.split(line;"},");
```
Splits input on object boundaries, assuming `"},` separates JSON objects.

```toke
let idpart=s.split(obj;"\"id\":\"");
```
Locates ID field by splitting on the literal pattern `"id":"`.

```toke
let idsplit=s.split(after;"\"");idval=idsplit.get(0)
```
Extracts ID value by splitting on closing quote and taking first segment.

```toke
lp(let j=0;j<seen.len;j=j+1){if(seen.get(j)=idval){isdup=true}}
```
Linear search through seen IDs (no hash table available).

```toke
if(k>0){out=s.concat(out;"},")};
```
Conditionally adds delimiter between objects during reconstruction.

## Test Coverage

**Recommended Test Cases:**
- **Basic Deduplication**: Objects with same ID values
- **No Duplicates**: All unique IDs 
- **Edge Cases**: Empty input, malformed JSON, missing ID fields
- **Boundary Conditions**: Single object, all duplicates
- **ID Variations**: Different ID formats, special characters in IDs

## Complexity

**Time Complexity**: O(n²) where n = number of objects
- ID extraction: O(n) 
- Duplicate detection: O(n²) due to linear search for each object
- Output reconstruction: O(n)

**Space Complexity**: O(n)
- Stores all unique objects and IDs in memory
- Temporary string allocations during processing

## Potential Improvements

1. **Performance**: Implement hash-based lookup for O(n) duplicate detection instead of O(n²) linear search
2. **Robustness**: Add proper JSON parsing instead of string manipulation to handle edge cases
3. **Error Handling**: Validate input format and handle malformed objects gracefully
4. **Memory Efficiency**: Stream processing for large datasets instead of loading everything into memory
5. **Code Organization**: Extract ID parsing into separate function for reusability and testing
6. **Output Format**: Make output format configurable (pretty-print vs. compact JSON)
7. **Logging**: Add verbose mode to show which specific objects were removed