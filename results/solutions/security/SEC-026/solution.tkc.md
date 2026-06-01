# whoislookup.tkc.md

## Overview

This toke program simulates a basic domain classification system that analyzes user input to determine domain type. It reads a domain string from standard input and categorizes it as either a "registrant" (for .com domains) or "organization" (for all other domain types including .org and non-domain inputs).

## Architecture

```
main() function
├── Input Processing (trim user input)
├── Domain Validation (check for dot presence)
├── TLD Classification Logic
│   ├── .com detection → "registrant"
│   └── .org/.other detection → "organization"
└── Return (exit code 0)
```

**Modules Used:**
- `std.io` - Standard input/output operations
- `std.str` - String manipulation utilities

**Data Flow:** User Input → String Processing → Pattern Matching → Classification Output

## Key Concepts

- **Module Aliasing**: Demonstrates toke's module import with custom aliases (`io:std.io`, `s:std.str`)
- **String Methods**: Utilizes standard library string functions (`trim`, `contains`)
- **Conditional Logic**: Nested if-else statements for domain classification
- **Function Return Types**: Explicit `$i64` return type annotation
- **Standard I/O**: Interactive program using `readln()` and `println()`

## Line-by-Line Notes

```toke
m=whoislookup;                    // Module declaration
i=io:std.io;i=s:std.str;         // Import and alias standard libraries (io, string)
f=main():$i64{                   // Main function definition with i64 return type
  let input=s.trim(io.readln()); // Read and trim user input
  if(s.contains(input;".")){     // Check if input contains a dot (domain validation)
    if(s.contains(input;"com")){ // Check for .com TLD
      io.println("registrant")  // Output for commercial domains
    }el{
      if(s.contains(input;"org")){ // Check for .org TLD
        io.println("organization") // Output for org domains
      }el{
        io.println("organization") // Default for other domains with dots
      }
    }
  }el{
    io.println("organization")   // Output for non-domain inputs
  }
  ;<0                           // Statement separator and return 0
}
```

## Test Coverage

**Recommended Test Cases:**
- ✅ `.com` domains → Should output "registrant"
- ✅ `.org` domains → Should output "organization"  
- ✅ Other TLD domains (`.net`, `.edu`) → Should output "organization"
- ✅ Non-domain strings → Should output "organization"
- ✅ Empty input → Should output "organization"
- ✅ Strings with dots but no TLD → Should output "organization"

## Complexity

**Time Complexity:** O(n) where n is the input string length
- String operations (`trim`, `contains`) are linear in string length

**Space Complexity:** O(1) 
- Only stores the input string, no additional data structures

## Potential Improvements

1. **Enhanced TLD Detection**: Use proper domain parsing instead of substring matching to avoid false positives (e.g., "compromise" contains "com")

2. **Comprehensive TLD Support**: Expand classification logic for more TLD types (.gov, .edu, .net, country codes)

3. **Input Validation**: Add robust domain format validation (regex patterns, length checks)

4. **Error Handling**: Implement proper error handling for invalid inputs and I/O failures

5. **Configuration**: Make domain classifications configurable rather than hardcoded

6. **Code Structure**: Refactor nested conditionals into a cleaner pattern matching or lookup table approach

7. **Real WHOIS Integration**: Connect to actual WHOIS APIs for authentic domain information retrieval