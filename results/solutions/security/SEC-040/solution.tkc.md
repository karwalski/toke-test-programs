# CSP Scan Tool Documentation (.tkc.md)

## Overview

This program scans Content Security Policy (CSP) directives from standard input to detect potentially unsafe inline script configurations. It reads a single line of input and outputs either "unsafe-inline" if the dangerous directive is found, or "score" otherwise, making it useful for security auditing of web applications.

## Architecture

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   stdin     │───▶│  CSP Parser  │───▶│   stdout    │
│  (CSP line) │    │   (main())   │    │ (result)    │
└─────────────┘    └──────────────┘    └─────────────┘
```

**Module Structure:**
- **cspscan**: Main module containing the scanning logic
- **std.io**: Standard I/O operations for input/output handling
- **std.str**: String manipulation utilities for pattern matching

**Data Flow:**
1. Read CSP directive line from stdin
2. Search for `'unsafe-inline'` pattern in the input
3. Output classification result to stdout
4. Return exit code 0

## Key Concepts

**Toke Language Features Demonstrated:**
- **Module System**: Imports with aliasing (`io:std.io`, `s:std.str`)
- **Function Declaration**: Main entry point with explicit return type (`$i64`)
- **Type System**: Implicit string typing with explicit integer return
- **Standard Library Usage**: I/O and string manipulation functions
- **Control Flow**: Conditional branching with `if`/`el` syntax
- **Variable Binding**: Local variable declaration with `let`

## Line-by-Line Notes

```toke
m=cspscan;
```
Module declaration establishing the namespace.

```toke
i=io:std.io;i=s:std.str;
```
Import aliases: `io` for I/O operations, `s` for string functions. Note the compact syntax with semicolon separation.

```toke
f=main():$i64{
```
Main function declaration with explicit `i64` return type (standard for exit codes).

```toke
let line=io.readln();
```
Read one line from stdin, storing in immutable `line` variable.

```toke
if(s.contains(line;"'unsafe-inline'")){io.println("unsafe-inline")}
```
Pattern matching for the literal string `'unsafe-inline'` (including quotes), which indicates unsafe CSP configuration.

```toke
el{io.println("score")}
```
Default case output - possibly indicating a "scoring" or evaluation mode when no unsafe directives are found.

```toke
;<0}
```
Statement terminator and return value 0 (successful execution).

## Test Coverage

**Recommended Test Cases:**
- **Positive Detection**: CSP headers containing `'unsafe-inline'`
- **Negative Cases**: Clean CSP directives without unsafe inline permissions
- **Edge Cases**: Empty input, malformed CSP syntax
- **Variant Testing**: Different quote styles, spacing variations

**Example Test Scenarios:**
```
Input: "script-src 'self' 'unsafe-inline'"
Expected: "unsafe-inline"

Input: "script-src 'self' 'strict-dynamic'"
Expected: "score"
```

## Complexity

**Time Complexity:** O(n) where n is the length of the input line
- Single pass string search operation
- Linear scan through input characters

**Space Complexity:** O(n) for input line storage
- One string buffer for the complete input line
- Constant space for pattern matching

## Potential Improvements

1. **Enhanced Pattern Matching**: Support multiple unsafe CSP directives (`'unsafe-eval'`, `'unsafe-hashes'`)

2. **Robust Input Handling**: Process multiple lines or entire CSP headers across multiple inputs

3. **Detailed Reporting**: Output specific unsafe directive types and positions rather than binary classification

4. **Error Handling**: Graceful handling of I/O errors or malformed input

5. **Configuration**: Command-line flags for different scanning modes or custom pattern lists

6. **Output Formatting**: JSON or structured output for integration with security tools

7. **Performance**: Stream processing for large files rather than line-by-line reading