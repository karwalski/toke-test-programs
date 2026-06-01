# Bitcoin Transaction Size Calculator - Companion Documentation

## Overview

This toke program calculates Bitcoin transaction metrics, specifically the transaction weight and virtual bytes (vbytes) given legacy and witness input counts. It implements the BIP 141 SegWit transaction size calculation formula where legacy inputs are weighted 4x and witness data is counted at face value.

## Architecture

The program follows a simple two-function architecture:

- **Module imports**: `txsize`, `std.io`, and `std.str` for I/O and string operations
- **`solve()` function**: Core calculation logic for weight and vbytes computation
- **`main()` function**: I/O handler that reads inputs, calls solver, and outputs results
- **Data flow**: Input → Parse → Calculate → Format → Output

## Key Concepts

- **Type system**: Explicit type annotations (`$i64`) for function parameters and returns
- **Immutable/mutable variables**: Uses `let` for immutable bindings and `mut` for mutable operations
- **Standard library usage**: Demonstrates `std.io` for I/O operations and `std.str` for string conversions
- **Conditional logic**: Integer comparison and branching with `if` statements
- **Function composition**: Separation of pure calculation logic from I/O concerns

## Line-by-Line Notes

```toke
let weight=legacy*4+witness;
```
Implements BIP 141 weight calculation: legacy inputs cost 4 weight units each, witness data costs 1.

```toke
let vbytes=mut.weight/4;
```
Virtual bytes calculation via integer division (truncates remainder).

```toke
let rem=weight-vbytes*4;if(!(rem=0)){vbytes=vbytes+1};
```
Manual ceiling operation: if there's a remainder after division, round up by adding 1 to vbytes.

```toke
let weight=legacy*4+witness;
```
Weight calculation is duplicated in `main()` for output purposes, though it could reference the `solve()` result.

## Test Coverage

The current implementation lacks explicit test cases. Recommended test scenarios:

- **Edge cases**: Zero legacy/witness inputs
- **Exact division**: Weight perfectly divisible by 4  
- **Remainder handling**: Weight with 1, 2, 3 remainder when divided by 4
- **Large inputs**: Verify no integer overflow
- **Real transaction examples**: Compare against known Bitcoin transaction metrics

## Complexity

- **Time complexity**: O(1) - constant time arithmetic operations
- **Space complexity**: O(1) - fixed number of integer variables
- **I/O complexity**: O(1) - reads exactly two lines, writes exactly two lines

## Potential Improvements

1. **DRY principle**: Eliminate weight calculation duplication between functions
2. **Error handling**: Add input validation for negative numbers and non-integer inputs
3. **Documentation**: Add inline comments explaining Bitcoin-specific terminology
4. **Return structure**: `solve()` could return both weight and vbytes as a tuple/struct
5. **Function naming**: More descriptive names like `calculate_transaction_metrics()`
6. **Input format**: Support single-line input or command-line arguments
7. **Unit tests**: Add comprehensive test suite covering edge cases
8. **Output formatting**: Consider structured output (JSON) or labeled values