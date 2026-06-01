# jobseq.tkc.md

## Overview

This Toke program implements a job scheduling algorithm that reads job data from standard input and outputs an optimal sequence using the Shortest Processing Time (SPT) rule. The program calculates the makespan (total completion time) and counts how many jobs finish late relative to their due dates, outputting results in JSON format.

## Architecture

The program follows a linear single-function design with three main phases:

1. **Input Processing** — Reads CSV-formatted job data (name, processing time, due date) from stdin
2. **SPT Scheduling** — Sorts jobs by processing time using selection sort to create optimal sequence
3. **Output Generation** — Calculates metrics and formats results as JSON

Data is stored in parallel mutable arrays (`names`, `times`, `dues`) with indices maintained through an `order` array that gets sorted.

## Key Concepts

- **Mutable Collections**: Demonstrates `mut.@()` for dynamic arrays and element appending with `+@()`
- **String Processing**: Heavy use of `std.str` module for parsing, concatenation, and type conversion
- **Standard I/O**: Uses `std.io` for line-by-line input reading and output
- **Control Flow**: Nested loops with manual array manipulation and conditional logic
- **Type Coercion**: String-to-integer conversion for numeric job parameters

## Line-by-Line Notes

**Input Loop** (`lp(let lineidx=0;lineidx<100;lineidx=lineidx+1)`):
- Reads up to 100 lines, breaking on empty input
- Skips header lines containing "job,"
- Splits CSV and validates minimum 3 fields before storing

**Selection Sort** (nested loops starting with `lp(let i=0;i<n;i=i+1)`):
- Finds minimum processing time in remaining unsorted portion
- Manually reconstructs `order` array by copying elements and swapping positions
- Implements SPT scheduling which minimizes mean completion time

**Metrics Calculation**:
- `makespan`: Sum of all processing times (total schedule length)
- `late`: Count of jobs where completion time exceeds due date
- `current`: Running sum to track individual job completion times

**JSON Construction**:
- Manual string concatenation to build valid JSON output
- Quoted job names in sequence array, numeric values for metrics

## Test Coverage

Ideal test cases should verify:
- **Empty input** — Handles no jobs gracefully
- **Single job** — Correct trivial scheduling
- **Multiple jobs** — SPT ordering with various processing times
- **Due date scenarios** — Jobs finishing early/late/on-time
- **Malformed input** — CSV parsing edge cases and invalid data
- **JSON format** — Valid output structure and syntax

## Complexity

- **Time**: O(n²) due to selection sort implementation, where n is number of jobs
- **Space**: O(n) for storing job data in parallel arrays
- **I/O**: O(m) where m is total input lines (bounded by 100)

The SPT algorithm itself is optimal for minimizing mean completion time, but could be implemented more efficiently.

## Potential Improvements

1. **Performance**: Replace selection sort with O(n log n) sorting algorithm
2. **Code Structure**: Extract functions for parsing, sorting, and output formatting
3. **Error Handling**: Add validation for malformed CSV and invalid numeric data
4. **Memory Efficiency**: Use single array of job structs instead of parallel arrays
5. **Input Flexibility**: Remove arbitrary 100-line limit and support larger datasets
6. **Algorithm Options**: Support multiple scheduling objectives (earliest due date, etc.)
7. **JSON Library**: Use proper JSON serialization instead of manual string building