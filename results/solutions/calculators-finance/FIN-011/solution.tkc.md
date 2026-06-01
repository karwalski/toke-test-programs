# Compound Interest Calculator - Documentation

**File:** `compoundinterest.tkc.md`

## Overview

This program calculates compound interest using the standard mathematical formula A = P(1 + r/n)^(nt). It reads input parameters from standard input and outputs the final amount with compound interest applied, formatted to two decimal places.

## Architecture

The program is structured as a single module with two main functions:

- **`compoundinterest()`** — Core calculation function that implements the compound interest formula
- **`main()`** — Entry point that handles I/O, input parsing, and result formatting

**Data Flow:**
```
Input (stdin) → Parse parameters → Calculate compound interest → Format result → Output (stdout)
```

**Dependencies:**
- `std.io` — Input/output operations
- `std.str` — String manipulation and parsing
- `std.math` — Mathematical operations (power function)

## Key Concepts

### Type System Features
- **Type casting:** `time as $f64` and `compfreq as $f64` demonstrate explicit type conversion
- **Strong typing:** Clear distinction between `$f64` (floating-point) and `$i64` (integer) parameters
- **Function signatures:** Explicit parameter and return type declarations

### Standard Library Usage
- **String operations:** `split()`, `tofloat()`, `toint()`, `format()`
- **I/O operations:** `readln()`, `println()`
- **Math functions:** `pow()` for exponentiation

### Language Patterns
- **Module aliasing:** `i=io:std.io` pattern for namespace management
- **Let bindings:** Immutable variable declarations with `let`
- **Function definitions:** `f=functionname()` syntax

## Line-by-Line Notes

### Module Declarations
```toke
m=compoundinterest;i=io:std.io;i=s:std.str;i=math:std.math;
```
- Declares module name and imports with aliases (note: `i=s:std.str` overwrites `io` alias)

### Compound Interest Function
```toke
let t=time as $f64;let n=compfreq as $f64;
```
- Converts integer inputs to floating-point for mathematical operations

```toke
let base=1.0+rate/n;let exponent=n*t;
```
- Separates compound interest formula components for clarity
- `base` = (1 + r/n), `exponent` = n×t

### Main Function Input Parsing
```toke
let parts=s.split(line;" ");
```
- Splits space-delimited input into array of strings

```toke
if(parts.len()>=4){...}
```
- Validates minimum required parameters before processing

```toke
io.println(s.format(result;"%.2f"))
```
- Formats output to 2 decimal places using printf-style formatting

## Test Coverage

To thoroughly test this program, verify:

1. **Valid inputs:** Various combinations of principal, rate, frequency, and time
2. **Edge cases:** 
   - Zero principal amount
   - Zero interest rate
   - Single compounding period
   - Very large time periods
3. **Input validation:**
   - Insufficient parameters (< 4 values)
   - Invalid number formats
   - Negative values
4. **Output formatting:** Results display exactly 2 decimal places

**Sample Test:**
```
Input: "1000 0.05 12 3"
Expected Output: "1161.62"
```

## Complexity

- **Time Complexity:** O(log n) due to `math.pow()` operation
- **Space Complexity:** O(1) for calculations, O(n) for input string parsing where n is input length

The computational bottleneck is the power function; all other operations are constant time.

## Potential Improvements

1. **Error Handling:** Add validation for negative values and division by zero scenarios
2. **Input Format:** Support multiple input formats (JSON, CSV) or interactive prompts
3. **Precision:** Use decimal arithmetic library for financial calculations to avoid floating-point errors
4. **Output Options:** Add options for different formatting (currency symbols, different decimal places)
5. **Code Organization:** Split into separate parsing and calculation modules for better maintainability
6. **Documentation:** Add inline comments and usage examples
7. **Performance:** Cache power calculations for repeated computations with same base/exponent