# HTTP Request Format Handler - Companion Documentation

## Overview

This program reads a URL and format specification from the user, determines the appropriate HTTP Accept header based on the format, and outputs the beginning of a structured response. It demonstrates basic input processing, conditional logic, and format-specific output generation in the Toke language.

## Architecture

```
Input Layer:
├── URL reading (line 1)
└── Format specification reading (line 2)

Processing Layer:
├── Accept header determination (conditional logic)
└── Format validation (string matching)

Output Layer:
├── Accept header decision
└── Format-specific response starter
```

**Modules:**
- `main` - Core program logic
- `std.io` - Input/output operations
- `std.str` - String manipulation utilities

**Data Flow:**
1. Read user inputs (URL, format)
2. Parse format string to determine content type
3. Set appropriate Accept header
4. Output format-specific response opening

## Key Concepts

**Toke Language Features Demonstrated:**
- **Module imports with aliasing** - `i=io:std.io;i=str:std.str`
- **Mutable variables** - `let accept=mut."text/plain"`
- **String literals and concatenation**
- **Conditional expressions** - nested `if/el` blocks
- **Standard library usage** - `str.contains()`, `io.readln()`, `io.println()`
- **Function return types** - `$i64`

**Type System:**
- String handling with `str` module
- Mutable string assignment
- Integer return type (`$i64`)

## Line-by-Line Notes

```toke
m=main;                           // Module alias for main
i=io:std.io;                     // Import std.io as 'io'
i=str:std.str;                   // Import std.str as 'str' (overwrites 'io' alias)
f=main():$i64{                   // Function 'f' returns i64
  let url=io.readln();           // Read URL from stdin (note: 'io' undefined after overwrite)
  let format=io.readln();        // Read format specification
  let accept=mut."text/plain";   // Mutable accept header, default to plain text
  
  if(str.contains(format;"json")){ // Check if format contains "json"
    accept="application/json"     // Set JSON accept header
  }el{
    if(str.contains(format;"xml")){ // Nested check for XML
      accept="application/xml"     // Set XML accept header
    }el{
      accept="text/plain"          // Default fallback
    }
  };
  
  if(str.contains(format;"json")){ // Duplicate JSON check for output
    io.println("{")               // JSON response opener
  }el{
    io.println("<")               // XML/HTML response opener  
  };
  
  <0                              // Return 0
}
```

## Test Coverage

**Recommended Test Cases:**
1. **JSON format input** - Verify "application/json" header and "{" output
2. **XML format input** - Verify "application/xml" header and "<" output  
3. **Plain text format** - Verify "text/plain" header and "<" output
4. **Mixed format strings** - Test "json-api", "xml-rpc", etc.
5. **Case sensitivity** - Test "JSON", "Json", "XML" variations
6. **Empty format string** - Verify default behavior

**Current Coverage Gaps:**
- No validation of URL format
- No error handling for invalid input
- Accept header is set but never output or used

## Complexity

**Time Complexity:** O(n) where n is the length of the format string
- `str.contains()` operations are linear in string length
- Two sequential string searches in worst case

**Space Complexity:** O(1) 
- Fixed number of string variables regardless of input size
- No dynamic data structures used

## Potential Improvements

### Code Quality
1. **Fix module aliasing bug** - `i=str:std.str` overwrites the `io` alias, making subsequent `io.readln()` calls undefined
2. **Eliminate duplicate logic** - The JSON format check is performed twice
3. **Use consistent naming** - Function should be named `main` instead of `f`

### Functionality  
4. **Output the Accept header** - Currently calculated but never displayed
5. **Add URL validation** - Verify URL format and structure
6. **Support more content types** - Add support for HTML, CSV, etc.
7. **Case-insensitive matching** - Handle "JSON", "Json", "XML" variants
8. **Complete response formatting** - Generate full HTTP request headers

### Error Handling
9. **Input validation** - Handle empty or malformed inputs gracefully
10. **Return meaningful exit codes** - Use different codes for different scenarios

### Suggested Refactor
```toke
// Fix aliasing and add proper structure
io=io:std.io; str=str:std.str;
main=main():$i64{
  let url=io.readln();
  let format=str.lower(io.readln());
  let accept=determineAcceptHeader(format);
  io.println("Accept: " + accept);
  outputResponseStart(format);
  <0
}
```