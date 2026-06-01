# tail.tkc.md

## Overview

This is a compact implementation of the Unix `tail` command that reads the last N lines from input and displays them with a labeled header. The program accepts a line count and an optional service label, then outputs a descriptive header before displaying the filtered content.

## Architecture

**Single Module Design:**
- `m=tail` - Main module declaration
- Two standard library imports: `io` (I/O operations) and `str` (string manipulation)
- Single entry point `main()` function that handles all logic inline
- Linear execution flow: input → processing → output

**Data Flow:**
```
User Input (count) → User Input (service) → Label Processing → Header Generation → Output
```

## Key Concepts

**Toke Language Features Demonstrated:**
- **Module system**: Standard library imports (`std.io`, `std.str`)
- **Type annotations**: Explicit `$i64` return type
- **Mutable variables**: `mut` keyword for modifiable label
- **String manipulation**: Extensive use of `concat()` operations
- **Type conversion**: `toint()` and `fromint()` for string/integer conversion
- **Conditional logic**: Simple if-statement for default value handling
- **Method chaining**: Nested function calls for string building

## Line-by-Line Notes

```toke
m=tail;                                    // Module declaration
i=io:std.io;i=s:std.str;                  // Import aliases (note: 'i' reused)
f=main():$i64{                            // Function declaration with return type
  let n=s.toint(io.readln());             // Read line count as integer
  let svc=s.trim(io.readln());            // Read and trim service name
  let label=mut."syslog";                 // Mutable default label
  if(s.len(svc)>0){label=svc};            // Override if service provided
  io.println(s.concat(s.concat(           // Complex nested string concatenation
    s.concat("(last ";s.fromint(n));      // Build: "(last N"
    " ");                                  // Add space
    s.concat(label;" lines)")));           // Add: "label lines)"
  <0                                       // Return 0 (success)
}
```

**Notable Issues:**
- Variable `i` is reassigned from `io` to `str`, potentially confusing
- Missing semicolon before return statement
- Heavy nesting could impact readability

## Test Coverage

**Recommended Test Cases:**
- **Basic functionality**: Input count=10, service="nginx" → "(last 10 nginx lines)"
- **Default label**: Input count=5, empty service → "(last 5 syslog lines)"
- **Edge cases**: 
  - Zero count: count=0 → "(last 0 syslog lines)"
  - Large numbers: count=1000
  - Whitespace handling: service with leading/trailing spaces
- **Error cases**: Invalid number format, negative counts

## Complexity

**Time Complexity:** O(n) where n is the total length of input strings
- String operations (`trim`, `concat`, `fromint`) are linear
- Conditional check is O(1)

**Space Complexity:** O(m) where m is the combined length of all string variables
- Stores: `n`, `svc`, `label`, and intermediate concatenation results
- Multiple temporary strings created during nested `concat()` calls

## Potential Improvements

**Code Quality:**
- **Variable naming**: Use distinct names instead of reusing `i`
- **String building**: Use string interpolation if available, or intermediate variables
- **Formatting**: Add proper spacing and line breaks for readability

**Functionality Enhancements:**
- **Input validation**: Check for negative numbers or invalid input
- **Error handling**: Graceful handling of malformed input
- **Actual tail logic**: Currently only generates header; missing file reading/line filtering
- **Configurability**: Support for different output formats or file input

**Performance:**
- **String concatenation**: Reduce nested calls with string builder pattern
- **Memory optimization**: Minimize intermediate string creation

**Example Refactored Structure:**
```toke
let header = format("(last {} {} lines)", n, label);
io.println(header);
```