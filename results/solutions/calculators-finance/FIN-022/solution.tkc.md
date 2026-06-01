# GST Calculator - Companion Documentation (.tkc.md)

## Overview

This toke program implements a simple GST (Goods and Services Tax) calculator that computes the total price including tax for a given amount and tax rate. The program calculates GST for a base amount of $100.00 with a 10% tax rate and displays both the original amount and the calculated GST amount.

## Architecture

The program consists of two main functions:
- **`gst()`** - Core calculation function that applies tax rate to a base amount
- **`main()`** - Entry point that sets up test values and handles output formatting

**Data Flow:**
```
Input Values (rate, amount) → gst() → Total Calculation → main() → Formatted Output
```

**Module Dependencies:**
- `std.io` - For console output operations
- `std.str` - For string formatting functions

## Key Concepts

**Toke Language Features Demonstrated:**
- **Module Imports:** Multiple standard library imports with aliasing (`io:std.io`, `s:std.str`)
- **Function Definition:** Custom function with typed parameters and return values
- **Type System:** Explicit type annotations (`$f64`, `$i64`) 
- **Mutable Variables:** Use of `mut` keyword for variable mutation
- **Conditional Logic:** `if-el` branching structure
- **Standard Library Usage:** String formatting and I/O operations

## Line-by-Line Notes

| Section | Explanation |
|---------|-------------|
| `m=gst;i=io:std.io;i=s:std.str` | Module alias setup and standard library imports |
| `let result=mut.0.0` | Initialize mutable result variable to 0.0 |
| `if(rate>0.0){let gstamt=amount*rate;result=amount+gstamt}` | Calculate GST only if rate is positive; add tax to base amount |
| `el{result=amount}` | Fallback: return original amount if rate is non-positive |
| `s.format(amount;"%.2f")` | Format floating-point numbers to 2 decimal places |

## Test Coverage

The current implementation includes basic functionality testing:

**Covered Scenarios:**
- ✅ Positive tax rate calculation (10% GST)
- ✅ Basic amount formatting and display
- ✅ Standard mathematical operations

**Missing Test Cases:**
- ❌ Zero tax rate handling
- ❌ Negative tax rate validation  
- ❌ Edge cases (very large/small amounts)
- ❌ Invalid input handling

## Complexity

**Time Complexity:** O(1) - Constant time operations (arithmetic and conditionals)  
**Space Complexity:** O(1) - Fixed memory usage regardless of input size

## Potential Improvements

### Code Quality
- **Error Handling:** Add validation for negative amounts or invalid rates
- **Modularity:** Separate calculation logic from presentation logic
- **Documentation:** Add inline comments explaining business logic

### Functionality  
- **Input Validation:** Implement bounds checking for tax rates (0-100%)
- **Multiple Tax Types:** Support for different tax categories (VAT, sales tax, etc.)
- **Currency Support:** Handle different currency formats and locales
- **Precision:** Use decimal types instead of floating-point for financial calculations

### Testing
- **Unit Tests:** Comprehensive test suite covering edge cases
- **Integration Tests:** End-to-end workflow validation
- **Property Testing:** Verify mathematical properties (e.g., commutativity)

### Performance
- **Batch Processing:** Support calculating GST for multiple items
- **Caching:** Memoize frequently used rate calculations