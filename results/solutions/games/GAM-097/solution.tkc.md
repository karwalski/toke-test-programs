# poker.tkc.md

## Overview

This is a poker pot odds calculator that reads betting information from user input and computes the pot odds percentage. The program calculates both the pot odds and the minimum equity required to make a profitable call in poker.

## Architecture

**Single Module Structure:**
- **Module:** `poker` (main module)
- **Imports:** Standard library modules for I/O (`std.io`), string operations (`std.str`), and math (`std.math`)
- **Entry Point:** `main()` function that returns `$i64`
- **Data Flow:** Input → Parse → Calculate → Output

**Function Organization:**
```
main()
├── Input handling (readln, split)
├── Validation (length check)
├── Calculation (pot odds formula)
└── Output formatting (percentage display)
```

## Key Concepts

**Toke Language Features Demonstrated:**
- **Module System:** Import aliasing (`i=io:std.io`, `i=s:std.str`, etc.)
- **Type System:** Explicit type casting (`as$f64`) and return type annotation (`$i64`)
- **String Operations:** Splitting, concatenation, and formatting
- **Error Handling:** Basic conditional validation with fallback
- **Standard Library Usage:** I/O operations, string manipulation, and mathematical operations

## Line-by-Line Notes

```toke
m=poker;                                    // Module declaration
i=io:std.io;i=s:std.str;i=math:std.math;   // Import std libs with aliases
f=main():$i64{                             // Main function returns 64-bit integer
    let line=io.readln();                  // Read user input line
    let parts=s.split(line;" ");           // Split input on spaces
    if(parts.len()>=2){                    // Validate minimum 2 arguments
        let pot=s.toint(parts.get(0));     // Parse pot size (first arg)
        let bet=s.toint(parts.get(1));     // Parse bet size (second arg)
        let totalafterbet=pot+bet;         // Calculate total pot after call
        let potodds=(bet as$f64*100.0)/(totalafterbet as$f64); // Pot odds formula
        let oddsstr=s.format(potodds;"%.2f"); // Format to 2 decimal places
        io.println(s.concat("Pot odds: ";s.concat(oddsstr;"%"))); // Output pot odds
        io.println(s.concat("Minimum equity: ";s.concat(oddsstr;"%"))); // Output equity
    }el{
        io.println("error")                // Error message for invalid input
    };
    <0                                     // Return 0 (success)
}
```

## Test Coverage

**Recommended Test Cases:**
- **Valid Input:** `"100 25"` → Should output `"Pot odds: 20.00%"` and `"Minimum equity: 20.00%"`
- **Edge Cases:** 
  - Single argument: `"100"` → Should output `"error"`
  - Empty input: `""` → Should output `"error"`
  - Non-numeric input: `"abc def"` → Runtime error (uncaught)
- **Mathematical Verification:** Various pot/bet combinations to verify formula accuracy

**Current Gaps:**
- No validation for non-numeric input
- No handling of negative numbers
- No validation for zero values

## Complexity

**Time Complexity:** O(n) where n is the length of the input string (due to string splitting)
**Space Complexity:** O(n) for storing the split string parts

**Mathematical Formula:**
```
Pot Odds = (Bet Size / (Pot Size + Bet Size)) × 100%
```

## Potential Improvements

1. **Error Handling:** Add validation for non-numeric input using try-catch or result types
2. **Input Validation:** Check for negative numbers and zero values
3. **Code Organization:** Extract calculation logic into separate functions for better modularity
4. **Output Formatting:** Consider more sophisticated formatting options
5. **Extended Features:** 
   - Support for multiple betting rounds
   - Implied odds calculation
   - Hand equity comparison
6. **Performance:** For single-use calculation, current performance is adequate, but could cache parsed values for batch processing
7. **User Experience:** Add input prompts and more descriptive error messages
8. **Documentation:** Add inline comments explaining the poker concepts for non-poker players