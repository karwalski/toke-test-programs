# Load Balancer Program Documentation (loadbalance.tkc.md)

## Overview

This Toke program implements a greedy load balancing algorithm that distributes jobs across multiple machines to minimize makespan (maximum completion time). It reads job specifications from standard input and outputs a JSON report showing the optimal job assignments, machine loads, and overall makespan.

## Architecture

The program follows a linear execution model with three main phases:

1. **Input Processing**: Parses CSV-formatted input to extract machine count and job specifications
2. **Job Sorting**: Implements a selection sort to order jobs by processing time (descending)
3. **Load Balancing**: Uses a greedy assignment strategy to distribute sorted jobs to machines
4. **Output Generation**: Constructs and prints a JSON report with assignment details

**Data Flow**: Raw CSV input → Parsed job list → Sorted job queue → Machine assignments → JSON output

## Key Concepts

- **Mutable Variables**: Extensive use of `mut` keyword for dynamic data structures
- **Array Operations**: Heavy reliance on Toke's array type `@()` with `.get()`, `.len()`, and concatenation
- **String Manipulation**: Uses `std.str` module for parsing, conversion, and output formatting
- **Standard I/O**: Leverages `std.io` for line-based input reading and output
- **Imperative Loops**: Implements `lp()` constructs for both conditional and counted iterations
- **Type System**: Demonstrates integer conversion with `s.toint()` and `s.fromint()`

## Line-by-Line Notes

**Lines 1-3**: Module imports with aliases (`io` for std.io, `s` for std.str)

**Lines 4-6**: Header parsing to extract machine count (defaults to 2 if not specified)

**Lines 7-15**: Input loop reading job data until empty line encountered, parsing CSV format

**Lines 16-27**: Selection sort implementation to order jobs by processing time (highest first)

**Lines 28-40**: Greedy assignment loop - each job goes to machine with current minimum load

**Lines 41-65**: JSON output construction using string concatenation, formatting machine assignments, loads, and calculating makespan

## Test Coverage

To properly test this program, verify:

- **Input Parsing**: Various CSV formats, missing machine counts, malformed data
- **Sorting Logic**: Jobs correctly ordered by processing time
- **Load Balancing**: Greedy assignment produces expected distributions
- **Edge Cases**: Single machine, single job, empty input, jobs with zero time
- **Output Format**: Valid JSON structure with correct assignments and makespan calculation

## Complexity

- **Time Complexity**: O(n² + nm) where n = number of jobs, m = number of machines
  - Selection sort: O(n²)
  - Job assignment: O(nm)
- **Space Complexity**: O(n + m) for storing job data and machine assignments
- **I/O Complexity**: Linear in input size plus JSON output generation

## Potential Improvements

1. **Algorithm Efficiency**: Replace selection sort with quicksort/mergesort for O(n log n) sorting
2. **Code Structure**: Extract functions for parsing, sorting, and assignment phases
3. **Error Handling**: Add validation for malformed CSV input and invalid numeric data
4. **Memory Optimization**: Use in-place sorting instead of creating new arrays
5. **Algorithm Quality**: Consider more sophisticated load balancing (e.g., longest processing time first with backtracking)
6. **Output Flexibility**: Support multiple output formats beyond JSON
7. **Input Sources**: Accept file input in addition to stdin
8. **Documentation**: Add inline comments for complex logic sections