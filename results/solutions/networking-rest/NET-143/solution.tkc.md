# TCP Echo Server - Companion Documentation

## Overview

This is a simple TCP echo server implementation in Toke that reads host and port configuration, then continuously reads input lines and echoes them back until an empty line is received. The program demonstrates basic I/O operations and control flow in a network service context.

## Architecture

The program follows a linear, procedural structure:

- **Module Imports**: Standard I/O and string manipulation libraries
- **Configuration Phase**: Reads host and port from user input
- **Echo Loop**: Continuously processes input lines until termination condition
- **Cleanup**: Outputs connection status and exits

Data flows unidirectionally from input → processing → output, with no complex state management or concurrent operations.

## Key Concepts

- **Module Aliasing**: Demonstrates Toke's module import and aliasing syntax (`m=main`, `i=io:std.io`)
- **Standard Library Usage**: Utilizes `std.io` for I/O operations and `std.str` for string manipulation
- **Mutable Variables**: Uses `mut` keyword for variables that change during execution
- **Control Flow**: Implements while loop with `lp()` construct and conditional logic
- **Function Return Types**: Explicit `$i64` return type annotation
- **Error Handling**: Simple exit code pattern (returns 0 for success)

## Line-by-Line Notes

```toke
m=main;i=io:std.io;i=s:std.str;
```
- Sets up module aliases: `m` for main, `io` for standard I/O, `s` for string operations
- Note: Second `i=` assignment appears to be a typo, should likely be separate variable

```toke
f=main():$i64{
```
- Defines main function with explicit 64-bit integer return type

```toke
let host=io.readln();let port=io.readln();
```
- Reads configuration values from standard input (immutable bindings)

```toke
let line=mut.io.readln();
```
- Initializes mutable line buffer for the echo loop

```toke
lp(s.len(line)>0){io.println(line);line=io.readln()};
```
- Core echo loop: continues while line length > 0, prints current line, reads next line

```toke
io.println("Connection closed");<0
```
- Cleanup message and successful exit (return code 0)

## Test Coverage

To properly test this program, verify:

1. **Configuration Input**: Host and port values are correctly read and stored
2. **Echo Functionality**: Non-empty lines are echoed exactly as received
3. **Termination Condition**: Empty line input properly exits the loop
4. **Output Format**: Connection closed message appears after loop termination
5. **Return Code**: Program exits with status 0

## Complexity

- **Time Complexity**: O(n) where n is the number of input lines
- **Space Complexity**: O(1) - constant memory usage regardless of input size
- **I/O Complexity**: Blocking I/O operations may impact performance under high load

## Potential Improvements

1. **Error Handling**: Add validation for host/port configuration and I/O failures
2. **Code Clarity**: Fix variable aliasing issue (`i=s:std.str` overrides `i=io:std.io`)
3. **Network Implementation**: Currently only simulates echo behavior - needs actual TCP socket handling
4. **Concurrent Support**: Add multi-client support with threading or async I/O
5. **Configuration**: Support command-line arguments or config files instead of interactive input
6. **Logging**: Add structured logging for debugging and monitoring
7. **Resource Management**: Implement proper socket cleanup and resource disposal
8. **Signal Handling**: Add graceful shutdown on SIGINT/SIGTERM
9. **Input Validation**: Sanitize and validate echo data for security
10. **Performance**: Consider buffered I/O for high-throughput scenarios