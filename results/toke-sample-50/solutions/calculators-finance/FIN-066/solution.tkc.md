# CAGR Calculator Documentation (.tkc.md)

## Overview

This Toke program calculates the Compound Annual Growth Rate (CAGR) for an investment or value over time. It reads three space-separated values from standard input (beginning value, ending value, and number of years) and outputs the annualized growth rate as a percentage with two decimal places.

## Architecture

**Module Structure:**
- **Main module**: `cagr` - Single-function calculator
- **Dependencies**: 
  - `std.io` - Input/output operations
  - `std.str` - String parsing and formatting
  - `std.math` - Mathematical operations (power function)

**Data Flow:**
1. Input → String parsing → Numeric conversion
2. CAGR calculation using financial formula
3. Formatting → Output

## Key Concepts

**Toke Language Features Demonstrated:**
- **Module imports with aliases**: Multiple `i=` statements for clean namespace management
- **Standard library usage**: IO operations, string manipulation, mathematical functions
- **Type system**: Implicit `$i64` return type, float arithmetic
- **Error handling**: Length validation with `if(parts.len>=3)`
- **Function chaining**: Method calls on parsed data structures

## Line-by-Line Notes

```toke
m=cagr;  // Module declaration
i=io:std.io;i=s:std.str;i=math:std.math;  // Import aliases for brevity
f=main():$i64{  // Main function returning 64-bit integer
  let line=io.readln();  // Read input line
  let parts=s.split(line;" ");  // Split on spaces into array
  if(parts.len>=3){  // Validate minimum 3 values present
    let beginning=s.tofloat(parts.get(0));  // Parse initial value
    let ending=s.tofloat(parts.get(1));     // Parse final value  
    let years=s.tofloat(parts.get(2));      // Parse time period
    let ratio=ending/beginning;             // Calculate total return ratio
    let exponent=1.0/years;                 // Calculate fractional exponent
    let growth=math.pow(ratio;exponent)-1.0; // Apply CAGR formula
    let percent=growth*100.0;               // Convert to percentage
    io.println(s.concat(s.format(percent;"%.2f");"%")) // Output formatted result
  };
  <0  // Return success code
}
```

## Test Coverage

**Recommended test cases should verify:**
- **Valid inputs**: Standard investment scenarios (e.g., "1000 1500 5")
- **Edge cases**: Zero/negative beginning values, single year periods
- **Input validation**: Insufficient parameters, non-numeric inputs
- **Precision**: Decimal accuracy for small growth rates
- **Boundary conditions**: Very large numbers, fractional years

## Complexity

**Time Complexity**: O(1) - Constant time arithmetic operations  
**Space Complexity**: O(n) where n is input line length for string processing  
**Mathematical Complexity**: Single power operation dominates runtime

## Potential Improvements

1. **Error Handling**: Add validation for negative/zero beginning values and non-numeric inputs
2. **Input Flexibility**: Support comma-separated values or different delimiters
3. **Output Options**: Allow custom precision or different output formats (decimal vs percentage)
4. **Documentation**: Add usage instructions and formula explanation
5. **Performance**: Pre-compile regex patterns if extending to batch processing
6. **Validation**: Add reasonable bounds checking (e.g., years > 0, realistic value ranges)
7. **Internationalization**: Support different locale number formats

**Formula Reference**: `CAGR = (Ending Value / Beginning Value)^(1/Years) - 1`