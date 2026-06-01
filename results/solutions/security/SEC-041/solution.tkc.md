# deserialiser.tkc.md

## Overview

This toke program implements a simple serialization format detector that analyzes input text to identify potentially dangerous serialization patterns. The program reads two lines of input, analyzes the second line for known serialization signatures, and outputs a classification result indicating the safety level of the detected format.

## Architecture

The program follows a simple linear architecture:
- **Module Declaration**: `deserialiser` module with standard library imports
- **Detection Logic**: `detect()` function containing pattern matching logic
- **Main Entry Point**: `main()` function orchestrating I/O and detection workflow

**Data Flow**: 
Input → Line Reading → Pattern Detection → Classification → Output

## Key Concepts

- **String Type System**: Demonstrates toke's `$str` type annotation for string parameters and return values
- **Standard Library Usage**: Imports and uses `std.io` for I/O operations and `std.str` for string manipulation
- **Conditional Logic**: Uses `if` statements for pattern matching without explicit `else` clauses
- **Function Return Values**: Shows both string returns (detection results) and integer returns (exit codes)
- **Variable Binding**: Uses `let` for immutable variable declarations

## Line-by-Line Notes

```toke
m=deserialiser;i=io:std.io;i=s:std.str;
```
Module declaration with aliased imports - `io` for I/O operations, `s` for string utilities.

```toke
f=detect(line2:$str):$str{if(s.contains(line2;"aced0005")){<"Java serialisation magic bytes"};
```
The `detect` function checks for Java serialization magic bytes (`0xACED0005` in hex format).

```toke
if(s.contains(line2;"__class__")){<"class hint"};
```
Detects Python pickle-style class hints which can indicate unsafe deserialization.

```toke
<"safe"}
```
Default return value when no dangerous patterns are detected.

```toke
let line1=io.readln();let line2=io.readln();
```
Reads two lines of input, though only `line2` is analyzed (line1 appears to be reserved for future use).

## Test Coverage

To properly test this program, verify:
- **Java Serialization Detection**: Input containing "aced0005" should return "Java serialisation magic bytes"
- **Python Pickle Detection**: Input containing "__class__" should return "class hint"  
- **Safe Input Handling**: Clean input should return "safe"
- **Edge Cases**: Empty strings, special characters, and mixed patterns
- **I/O Functionality**: Proper handling of stdin/stdout operations

## Complexity

- **Time Complexity**: O(n) where n is the length of the input line (due to string search operations)
- **Space Complexity**: O(1) additional space beyond input storage
- **Scalability**: Limited by single-line analysis approach

## Potential Improvements

1. **Enhanced Pattern Detection**: Add more serialization format signatures (Protocol Buffers, MessagePack, etc.)
2. **Multi-line Analysis**: Utilize the first input line or implement streaming analysis
3. **Severity Levels**: Replace binary safe/unsafe classification with risk scoring
4. **Error Handling**: Add validation for malformed input and I/O failures
5. **Configuration**: Make detection patterns configurable rather than hardcoded
6. **Performance**: Implement more efficient pattern matching for large inputs
7. **Logging**: Add diagnostic output for debugging detection logic
8. **Binary Analysis**: Support for actual binary data rather than hex string representations