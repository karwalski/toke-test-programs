# triangular.tkc.md

## Overview

This program detects triangular arbitrage opportunities in currency exchange rates. It reads exchange rate data from standard input, then checks if a specified three-currency cycle can generate profit through sequential currency conversions.

## Architecture

**Single Module Design:**
- `main()` function handles all logic sequentially
- **Input Phase:** Reads exchange rates until "CHECK" command
- **Processing Phase:** Extracts relevant rates for the three specified currencies
- **Analysis Phase:** Calculates arbitrage profit and outputs result

**Data Flow:**
```
Input Lines → Rate Storage → Rate Lookup → Arbitrage Calculation → Output
```

## Key Concepts

**Toke Language Features Demonstrated:**
- **Mutable Variables:** `mut.` prefix for dynamic data (`rates`, `checkline`, rate values)
- **Dynamic Arrays:** Using `@()` for rate storage with `.push()` method
- **Tuple/Array Access:** `.get(index)` pattern for data extraction
- **Standard Library Usage:** 
  - `std.io` for input/output operations
  - `std.str` for string manipulation (splitting, parsing, formatting)
  - `std.math` imported but unused
- **Control Flow:** `lp()` loops with break conditions
- **Type Conversion:** `s.tofloat()` for string-to-number conversion

## Line-by-Line Notes

**Input Processing:**
- `rates=mut.@()` initializes empty mutable array for storing rate tuples
- `lp(true)` creates infinite loop until "CHECK" command breaks execution
- Rate data stored as tuples: `@(from_currency, to_currency, rate_value)`

**Rate Extraction:**
- Uses `s.contains()` for flexible currency matching (allows partial string matches)
- Searches for three specific exchange paths: c1→c2, c2→c3, c3→c1
- Manual loop through rates array rather than using functional methods

**Arbitrage Calculation:**
- `product = r12 * r23 * r31` represents complete currency cycle
- Profit calculated as `(product - 1.0) * 100.0` for percentage
- Uses `s.format(profit, "%.2f")` for two-decimal formatting

## Test Coverage

**Input Validation:**
- Handles lines with insufficient parts (`parts.len() >= 3`)
- Validates CHECK command format (`checkparts.len() >= 4`)

**Rate Detection:**
- Tests currency code matching using substring containment
- Verifies correct rate assignment for each leg of triangle

**Output Scenarios:**
- **Profitable:** "ARBITRAGE X.XX%" where X.XX is profit percentage
- **Unprofitable:** "NO_ARBITRAGE" for product ≤ 1.0

## Complexity

**Time Complexity:** O(n) where n = number of exchange rates
- Single pass through rates for each currency pair lookup
- Three separate O(n) searches could be optimized

**Space Complexity:** O(n) for storing all exchange rates in memory

## Potential Improvements

**Code Organization:**
- Extract rate lookup logic into separate functions
- Add input validation for malformed rate values
- Use more descriptive variable names

**Performance Optimizations:**
- Build hash map/dictionary for O(1) rate lookups instead of O(n) linear search
- Single-pass rate extraction instead of three separate loops

**Functionality Enhancements:**
- Support bidirectional rates (auto-generate inverse rates)
- Handle multiple arbitrage opportunities in single dataset
- Add error handling for missing rates or invalid currency codes
- Consider floating-point precision issues in profit calculations

**Language Usage:**
- Remove unused `std.math` import
- Leverage more idiomatic Toke patterns if available (functional array methods)