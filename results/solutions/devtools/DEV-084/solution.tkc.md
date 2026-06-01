# AWS IAM Policy Validator - Toke Companion Documentation

## Overview

This program validates AWS IAM policy statements by analyzing JSON input for security risks. It specifically checks for overly permissive policies that grant all actions (`"Action":"*"`) or access to all resources (`"Resource":"*"`), outputting appropriate risk warnings or a "SECURE" confirmation.

## Architecture

The program follows a simple linear architecture:
- **Input Layer**: Reads policy JSON from stdin using `std.io`
- **Processing Layer**: Uses `std.str` string operations to parse and validate policy content
- **Output Layer**: Returns formatted risk assessment to stdout

**Data Flow**: JSON input → String parsing → Risk detection → Formatted output

## Key Concepts

- **Module Aliasing**: Demonstrates toke's module import system with aliases (`i=io:std.io`, `i=s:std.str`)
- **String Operations**: Extensive use of stdlib string functions (`contains`, `concat`, `len`)
- **Mutable Variables**: Uses `mut` keyword for the output string that gets built incrementally
- **Conditional Logic**: Multiple `if` statements for risk detection and output formatting
- **Type System**: Function signature specifies `$i64` return type (returns 0 for success)

## Line-by-Line Notes

```toke
m=validate;                                    // Module name declaration
i=io:std.io;i=s:std.str;                      // Import and alias I/O and string modules
f=main():$i64{                                // Main function returning 64-bit integer
  let line=io.readln();                       // Read entire input line as string
  let allaction=s.contains(line;"\"Action\":\"*\"");    // Check for wildcard actions
  let allresource=s.contains(line;"\"Resource\":\"*\""); // Check for wildcard resources  
  let out=mut."";                             // Mutable string builder for output
  if(allaction){                              // If wildcard action found
    out=s.concat(out;"RISK: Statement allows all actions (*)")
  };
  if(allresource){                            // If wildcard resource found
    if(s.len(out)>0){out=s.concat(out;"\n")}; // Add newline if previous risk exists
    out=s.concat(out;"RISK: Statement allows all resources (*)")
  };
  if(s.len(out)=0){out="SECURE"};            // Default to secure if no risks found
  io.println(out);                            // Output final assessment
  <0                                          // Return success code
}
```

## Test Coverage

Recommended test cases should verify:
- **Wildcard Action Only**: Input with `"Action":"*"` but specific resources
- **Wildcard Resource Only**: Input with `"Resource":"*"` but specific actions  
- **Both Wildcards**: Input containing both risk patterns
- **Secure Policy**: Input with specific actions and resources
- **Malformed JSON**: Edge cases with incomplete or invalid JSON structure
- **Empty Input**: Behavior with no input or empty strings

## Complexity

- **Time Complexity**: O(n) where n is the length of input JSON string (linear string scanning)
- **Space Complexity**: O(1) auxiliary space (excluding input/output strings)
- **Performance Notes**: Uses simple string contains operations rather than full JSON parsing for efficiency

## Potential Improvements

1. **JSON Parser Integration**: Replace string matching with proper JSON parsing for more robust validation
2. **Multiple Policy Support**: Handle arrays of policy statements rather than single-line input
3. **Comprehensive Risk Detection**: Check for other IAM security anti-patterns (overly broad service permissions, missing conditions)
4. **Error Handling**: Add validation for malformed JSON input with appropriate error messages
5. **Configuration**: Make risk patterns configurable rather than hardcoded
6. **Output Formatting**: Add structured output options (JSON, XML) for integration with other tools
7. **Logging**: Add debug/verbose modes for troubleshooting policy analysis