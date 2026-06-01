# Interest Calculator - Toke Program Documentation (.tkc.md)

## Overview

This program calculates simple interest and total amount based on user input of principal, rate, and time. It reads space-separated values from stdin, computes the financial calculations, and outputs the formatted results to stdout.

## Architecture

### Module Structure
- **Main module**: `interest` - Contains the core financial calculation logic
- **Dependencies**: 
  - `std.io` (aliased as `io`) - Input/output operations
  - `std.str` (aliased as `s`) - String manipulation utilities

### Function Hierarchy
```
main()
├── simpleinterest(principal, rate, time) → f64
└── totalamount(principal, interest) → f64
```

### Data Flow
1. Read input line from stdin
2. Parse space-separated values into principal, rate, time
3. Calculate simple interest using financial formula
4. Calculate total amount (principal + interest)
5. Output formatted results (2 decimal places)

## Key Concepts

### Toke Language Features Demonstrated
- **Module system**: `m=interest` declaration and stdlib imports with aliasing
- **Type annotations**: Explicit `$f64` and `$i64` type specifications
- **Function definitions**: `f=functionname(params):returntype{body}` syntax
- **Let bindings**: Immutable variable declarations with `let`
- **Expression-oriented**: Functions return expressions with `<expression>` syntax
- **Standard library usage**: String operations, I/O, and formatting
- **Conditional logic**: `if` statements with length validation

### Type System Usage
- `$f64` for floating-point financial calculations
- `$i64` for program exit codes
- Implicit type conversion through stdlib functions (`s.tofloat`)

## Line-by-Line Notes

```toke
m=interest;                              // Module declaration
i=io:std.io;i=s:std.str;                // Import aliases for I/O and string ops
f=simpleinterest(principal:$f64;rate:$f64;time:$f64):$f64{
    let interest=principal*rate*time;<interest  // Standard simple interest formula
};
f=totalamount(principal:$f64;interest:$f64):$f64{
    <principal+interest                  // Sum calculation
};
f=main():$i64{
    let line=io.readln();               // Read entire input line
    let parts=s.split(line;" ");        // Split on spaces into array
    if(parts.len()>=3){                 // Validate minimum 3 parameters
        let principal=s.tofloat(parts.get(0));  // Parse first value
        let rate=s.tofloat(parts.get(1));       // Parse second value  
        let time=s.tofloat(parts.get(2));       // Parse third value
        let interest=simpleinterest(principal;rate;time);
        let total=totalamount(principal;interest);
        io.println(s.format(interest;"%.2f"));  // Output interest (2 decimals)
        io.println(s.format(total;"%.2f"))      // Output total (2 decimals)
    };
    <0                                  // Return success exit code
}
```

## Test Coverage

### Input Validation Tests
- **Valid input**: "1000 0.05 2" → Should output interest and total
- **Insufficient parameters**: "1000 0.05" → Should handle gracefully (no output)
- **Invalid numbers**: "abc 0.05 2" → Depends on `s.tofloat` error handling

### Calculation Verification
- **Basic case**: Principal=1000, Rate=0.05, Time=2 → Interest=100.00, Total=1100.00
- **Zero values**: Test edge cases with 0 principal, rate, or time
- **Decimal precision**: Verify 2-decimal formatting works correctly

## Complexity

### Time Complexity
- **Overall**: O(n) where n is the length of input string
- **String parsing**: O(n) for split operation
- **Calculations**: O(1) for arithmetic operations
- **Formatting**: O(1) for float-to-string conversion

### Space Complexity
- **Overall**: O(n) for storing the split string parts
- **Variables**: O(1) additional space for numeric calculations

## Potential Improvements

### Error Handling
- Add validation for negative values (principal, rate, time should be ≥ 0)
- Handle `s.tofloat` conversion errors gracefully
- Provide user feedback for invalid input formats

### Input Flexibility  
- Support different delimiters (comma, tab)
- Allow optional whitespace around values
- Accept input prompts for better user experience

### Feature Enhancements
- Add compound interest calculation option
- Support multiple currency formatting
- Include input validation with descriptive error messages
- Add help/usage information

### Code Structure
- Extract input parsing into separate function
- Add parameter validation functions
- Consider using structured data types instead of individual parameters