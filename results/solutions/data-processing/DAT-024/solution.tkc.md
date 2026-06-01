# radixsort.tkc.md

## Overview

This program implements the radix sort algorithm with detailed visualization of each sorting pass. It reads a line of space-separated integers, sorts them using radix sort (starting from the ones digit), and displays the bucket contents after each digit position pass along with the final sorted result.

## Architecture

**Module Structure:**
- `radixsort` - Main module containing the sorting implementation
- `std.io` - Standard I/O operations for reading input and printing output  
- `std.str` - String manipulation utilities for parsing and formatting

**Function Organization:**
- `digitat(val, exp)` - Extracts digit at specific decimal position
- `maxof(arr)` - Finds maximum value in array to determine sorting passes needed
- `main()` - Orchestrates input parsing, radix sort execution, and output formatting

**Data Flow:**
1. Read and parse space-separated integers from input
2. Find maximum value to determine number of digit positions
3. For each digit position (ones, tens, hundreds, etc.):
   - Distribute numbers into 10 buckets based on current digit
   - Display bucket contents with labeled pass information
   - Collect numbers back from buckets in order
4. Output final sorted sequence

## Key Concepts

**Toke Language Features Demonstrated:**
- **Mutable variables**: `mut` keyword for variables that change during execution
- **Array operations**: Dynamic array construction with `@()`, concatenation with `+@()`
- **Type annotations**: Explicit typing with `$i64` for integers, `@$i64` for integer arrays
- **Loop constructs**: `lp()` for iterative processing with manual counter management
- **Module imports**: Aliased imports (`i=io:std.io`, `i=s:std.str`) for namespace management
- **String manipulation**: Extensive use of `s.concat()` for building formatted output strings

## Line-by-Line Notes

**Digit Extraction Logic:**
```toke
f=digitat(val:$i64;exp:$i64):$i64{<(val/exp)-((val/exp)/10)*10}
```
Uses integer division to isolate digit at position `exp` (1=ones, 10=tens, etc.)

**Bucket Management:**
```toke
let buckets=mut.@();lp(let b=0;b<10;b=b+1){buckets=buckets+@(@())}
```
Creates array of 10 empty sub-arrays representing digits 0-9

**Bucket Distribution:**
```toke
if(b=digit){bk=bk+@(val)}
```
Adds value to appropriate bucket based on current digit being processed

**Pass Labeling:**
```toke
let names=@("ones";"tens";"hundreds";"thousands";"tenthousands")
```
Human-readable labels for each digit position pass

## Test Coverage

**Input Scenarios to Verify:**
- Single digit numbers (basic bucketing)
- Multi-digit numbers with varying lengths
- Numbers with repeated digits
- Already sorted sequences
- Reverse sorted sequences
- Arrays with duplicate values

**Output Validation:**
- Correct bucket assignments for each pass
- Proper digit position labeling
- Final sorted order verification
- Empty bucket handling (buckets with no elements)

## Complexity

**Time Complexity:** O(d × (n + k))
- d = number of digits in maximum value
- n = number of elements  
- k = number of possible digit values (10 for decimal)

**Space Complexity:** O(n + k)
- Additional arrays for buckets and intermediate storage
- String concatenation creates temporary objects during output formatting

## Potential Improvements

**Performance Optimizations:**
- **String Builder Pattern**: Replace multiple `s.concat()` calls with more efficient string accumulation
- **In-Place Bucket Operations**: Minimize array copying during bucket collection phase
- **Early Termination**: Skip remaining passes if all numbers have been fully processed

**Code Quality Enhancements:**
- **Constant Definitions**: Extract magic numbers (10 for decimal base, bucket count)
- **Function Decomposition**: Split `main()` into smaller, focused functions (parseInput, formatOutput, etc.)
- **Error Handling**: Add validation for malformed input and integer overflow conditions
- **Configurable Base**: Generalize algorithm to support different radix bases beyond decimal

**Debugging Features:**
- **Intermediate State Logging**: Option to show array state before/after each pass
- **Performance Metrics**: Display pass count and element movement statistics