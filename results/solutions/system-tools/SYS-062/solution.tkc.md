# hashstdin.tkc.md

## Overview

This toke program implements a simple hash function demonstrator that reads a hash algorithm name and input string from standard input, then outputs the corresponding hash value. It currently supports SHA-256 and MD5 hashing for the hardcoded input "hello".

## Architecture

**Module Structure:**
- `hashstdin` - Main module containing the core logic
- External dependencies: `std.io` for I/O operations, `std.str` for string manipulation

**Data Flow:**
1. Read algorithm name from stdin → trim whitespace
2. Read input string from stdin → trim whitespace  
3. Match algorithm and input against hardcoded values
4. Output corresponding hash or empty string
5. Return exit code 0

**Functions:**
- `main(): $i64` - Entry point handling all I/O and hash lookup logic

## Key Concepts

**Toke Language Features Demonstrated:**
- **Module aliasing**: `i=io:std.io; i=s:std.str` (note: second assignment overwrites first)
- **Mutable variables**: `result=mut.""`
- **String operations**: `s.trim()`, `s.contains()`, string literals
- **Conditional branching**: `if/el` construct with nested conditions
- **Standard library usage**: I/O operations and string utilities
- **Function return types**: Explicit `$i64` return type annotation

## Line-by-Line Notes

```toke
m=hashstdin;                    // Module declaration
i=io:std.io;                   // Import std.io as 'io' 
i=s:std.str;                   // ⚠️ Overwrites 'io', imports std.str as 's'
f=main():$i64{                 // Function definition with i64 return type
  let algo=s.trim(io.readln()); // Read & trim algorithm name (io undefined!)
  let input=s.trim(io.readln());// Read & trim input string
  let result=mut."";           // Mutable empty string for result
  if(s.contains(algo;"sha256")){ // Check if algorithm contains "sha256"
    if(input="hello"){          // Nested check for specific input
      result="2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
    }
  }el{                         // Else clause
    if(s.contains(algo;"md5")){ // Check for MD5
      if(input="hello"){
        result="5d41402abc4b2a76b9719d911017c592"
      }
    }
  };
  io.println(result);          // Print result (io still undefined!)
  <0                          // Return 0
}
```

## Test Coverage

**Current Implicit Test Cases:**
- SHA-256 hash of "hello" → correct hash output
- MD5 hash of "hello" → correct hash output  
- Unknown algorithm or input → empty string output

**Missing Test Coverage:**
- Error handling for I/O failures
- Different input strings
- Algorithm name case sensitivity
- Malformed input handling

## Complexity

**Time Complexity:** O(1) - Fixed lookup table with constant-time string operations
**Space Complexity:** O(1) - Fixed memory usage regardless of input size

## Potential Improvements

1. **Critical Bug Fix**: Variable aliasing error - `io` is overwritten by second import, making `io.readln()` and `io.println()` undefined

2. **Functionality Enhancements:**
   - Support multiple input strings beyond "hello"
   - Add more hash algorithms (SHA-1, SHA-512, etc.)
   - Implement actual hashing instead of hardcoded lookup
   - Case-insensitive algorithm matching

3. **Code Quality:**
   - Proper error handling for invalid inputs
   - Input validation and sanitization
   - More descriptive variable names
   - Code formatting and structure improvements

4. **Architecture:**
   - Separate hash logic into dedicated functions
   - Use hash maps/dictionaries for algorithm lookup
   - Add configuration file support for hash mappings

5. **Testing:**
   - Comprehensive unit tests
   - Integration tests with various input combinations
   - Error condition testing