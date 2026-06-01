# Currency Converter - Toke Program Documentation

## Overview

This program implements a simple currency converter that reads currency conversion parameters and exchange rates from user input, then calculates and displays the converted amount. The program demonstrates basic I/O operations, string manipulation, and floating-point arithmetic in the Toke language.

## Architecture

The program consists of two main functions:

- **`convert()`** — Core conversion logic that multiplies an amount by an exchange rate
- **`main()`** — Entry point that handles input parsing, function orchestration, and output formatting

**Data Flow:**
1. Read two lines of input (amount/currencies and exchange rate)
2. Parse strings into structured data (amount, currency codes, rate)
3. Perform conversion calculation
4. Format and output result

**Module Dependencies:**
- `std.io` — Input/output operations
- `std.str` — String manipulation and parsing

## Key Concepts

- **Type System**: Demonstrates explicit type annotations (`$f64`, `$str`, `$i64`)
- **Standard Library Usage**: Heavy reliance on `std.str` for parsing and `std.io` for I/O
- **Function Parameters**: Multiple parameter passing with type safety
- **String Operations**: Splitting, array access, and type conversion from strings
- **Formatted Output**: Printf-style formatting for decimal precision

## Line-by-Line Notes

```toke
m=convert;i=io:std.io;i=s:std.str;
```
Module imports and aliasing. Note the reuse of `i` variable for different imports.

```toke
f=convert(amount:$f64;from:$str;to:$str;rate:$f64):$f64{let result=amount*rate;<result};
```
The `from` and `to` parameters are accepted but not used in the calculation—they could be used for validation or logging.

```toke
let parts1=s.split(input1;" ");let amount=s.tofloat(parts1.get(0));
```
Assumes first input line format: "amount from_currency to_currency"

```toke
let parts2=s.split(input2;" ");let rate=s.tofloat(parts2.get(2));
```
Assumes second input line format: "_ _ rate" (only third element is used)

```toke
io.println(s.format(result;"%.2f"));
```
Formats output to 2 decimal places for currency display.

## Test Coverage

To properly test this program, verify:

- **Valid Input**: Standard currency conversion with positive amounts and rates
- **Decimal Precision**: Ensure output rounds correctly to 2 decimal places
- **Edge Cases**: Zero amounts, very large/small numbers
- **Input Format**: Correct parsing of space-separated values
- **Error Handling**: Behavior with malformed input (though not explicitly handled)

## Complexity

- **Time Complexity**: O(1) — Linear operations only
- **Space Complexity**: O(1) — Fixed amount of variables regardless of input size
- **I/O Complexity**: 2 input reads, 1 output write

## Potential Improvements

1. **Error Handling**: Add validation for malformed input, invalid currency codes, negative amounts
2. **Currency Validation**: Use the `from` and `to` parameters to validate supported currency pairs
3. **Input Format Flexibility**: More robust parsing that handles varying input formats
4. **Rate Lookup**: Integration with a currency rate database instead of manual rate input
5. **Code Structure**: Better variable naming and code formatting for readability
6. **Multiple Conversions**: Support batch conversion operations
7. **Rounding Options**: Configurable decimal precision based on currency requirements
8. **Logging**: Add conversion history or transaction logging capabilities