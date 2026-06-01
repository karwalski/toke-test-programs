# cpuhist.tkc.md

## Overview

This Toke program creates a histogram of CPU utilization percentages by reading numerical values from input and categorizing them into 10% buckets (0-10%, 10-20%, etc.). It reads a count of values followed by space-separated CPU percentage data, then outputs a formatted histogram showing the distribution of CPU usage across the defined ranges.

## Architecture

The program consists of two main functions:
- **`bucket(v:$i64)`** — A classification function that maps CPU percentage values to bucket indices (0-9)
- **`main()`** — The primary logic that handles input parsing, bucket counting, and output formatting

**Data Flow:**
1. Read count and space-separated values from stdin
2. Parse each value and classify into buckets using the `bucket()` function
3. Accumulate counts in individual bucket variables (b0-b9)
4. Build formatted output string through repeated concatenation
5. Output the final histogram

## Key Concepts

- **Type System**: Demonstrates explicit type annotations (`$i64`) for function parameters and return values
- **Standard Library Usage**: 
  - `std.io` for input/output operations (`readln()`, `println()`)
  - `std.str` for string manipulation (`split()`, `trim()`, `toint()`, `fromint()`, `concat()`)
- **Mutable Variables**: Uses `mut` keyword for variables that change during execution
- **Loop Constructs**: Employs `lp()` for iteration with manual index management
- **Conditional Logic**: Extensive use of `if` statements for bucket classification and counting

## Line-by-Line Notes

```toke
f=bucket(v:$i64):$i64{...}
```
- Bucket function uses cascading if-statements instead of switch/match
- Returns bucket index 0-8 for values <90%, index 9 for ≥90%

```toke
let parts=s.split(s.trim(line);" ");
```
- Trims whitespace then splits on space character to handle input formatting

```toke
lp(let idx=0;idx<cnt;idx=idx+1){...}
```
- Manual loop with explicit index management (no foreach construct)
- Uses array-style access with `parts.get(idx)`

```toke
let out=mut."CPU% histogram: ";out=s.concat(out;...);
```
- Builds output string through sequential concatenation operations
- Each bucket result is formatted individually with labels

## Test Coverage

To properly test this program, verify:
- **Edge Cases**: Empty input, single values, boundary values (10, 20, 30, etc.)
- **Range Coverage**: Values in each 10% bucket to ensure correct classification
- **Input Validation**: Malformed input, non-numeric values, mismatched counts
- **Output Format**: Correct histogram labeling and count accuracy
- **Boundary Behavior**: Values exactly at bucket boundaries (e.g., 10%, 50%, 90%)

## Complexity

- **Time Complexity**: O(n) where n is the number of CPU values to process
- **Space Complexity**: O(n) for storing the split input array, plus O(1) for bucket counters
- **Bucket Classification**: O(1) with up to 9 conditional checks per value

## Potential Improvements

1. **Data Structures**: Replace individual bucket variables (b0-b9) with an array for cleaner code
2. **Error Handling**: Add validation for malformed input and out-of-range values
3. **Output Formatting**: Use a loop to generate histogram output instead of manual concatenation
4. **Bucket Function**: Consider using a mathematical approach (`v/10`) instead of cascading conditionals
5. **Input Flexibility**: Support reading from files or command-line arguments
6. **Visualization**: Add ASCII bar chart representation for better visual histogram display
7. **Performance**: For large datasets, consider streaming input instead of loading all values into memory