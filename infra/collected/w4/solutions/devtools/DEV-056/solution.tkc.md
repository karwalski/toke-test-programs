# logfilter.tkc.md

## Overview

This Toke program implements a log filtering utility that reads log entries from standard input and outputs only those matching or exceeding a specified severity level. The program first reads a minimum severity threshold, then processes log lines and filters them based on their severity levels (DEBUG < INFO < WARN < ERROR).

## Architecture

The program consists of two main functions:

- **`getsevlevel()`** — Maps severity strings to numeric levels for comparison
- **`main()`** — Orchestrates the filtering process with input reading and line processing

**Data Flow:**
1. Read minimum severity level from user
2. Convert to numeric level using `getsevlevel()`
3. Process each log line in a loop
4. Parse severity from log format and filter based on threshold
5. Output qualifying lines to stdout

## Key Concepts

- **Module System**: Uses qualified imports (`io:std.io`, `s:std.str`) with aliasing
- **Function Definition**: Demonstrates typed function signatures with `$str` and `$i64` types
- **Control Flow**: Uses `if` conditionals, `lp(true)` infinite loops, and `br` break statements
- **String Processing**: Leverages stdlib for trimming, splitting, and length operations
- **Array/Collection Access**: Uses `.get()` method and `.len` property for sequence manipulation

## Line-by-Line Notes

```toke
m=logfilter;
```
- Sets module name to `logfilter`

```toke
f=getsevlevel(sev:$str):$i64{...}
```
- Severity mapping function using cascading if statements
- Returns -1 for unrecognized severity levels

```toke
let parts=s.split(line;" ");
```
- Assumes log format where severity is the second space-delimited field
- Uses semicolon-space as delimiter (unusual but intentional)

```toke
if(parts.len>=2){...}
```
- Guards against malformed log lines with insufficient fields

```toke
if(level>=minlevel){io.println(line)}
```
- Core filtering logic: higher numeric levels indicate higher severity

## Test Coverage

Recommended test cases should verify:
- **Severity Parsing**: All four severity levels (DEBUG, INFO, WARN, ERROR) map correctly
- **Threshold Filtering**: Lines below threshold are filtered out, others pass through
- **Edge Cases**: Empty lines, malformed entries, unrecognized severity levels
- **Input Handling**: Whitespace trimming on threshold input
- **EOF Handling**: Program terminates cleanly on empty input

## Complexity

- **Time Complexity**: O(n×m) where n = number of log lines, m = average line length (due to string splitting)
- **Space Complexity**: O(m) for storing split line parts and temporary strings
- **I/O Bound**: Performance primarily limited by stdin/stdout operations rather than computation

## Potential Improvements

1. **Error Handling**: Add validation for malformed input and graceful error messages
2. **Configurable Format**: Support different log formats beyond space-delimited
3. **Case Sensitivity**: Make severity matching case-insensitive
4. **Performance**: Use streaming parser instead of full line splitting for large logs
5. **Additional Severities**: Support custom or extended severity levels (TRACE, FATAL, etc.)
6. **Regex Support**: Allow pattern-based filtering beyond simple severity levels
7. **Code Formatting**: Add whitespace and structure for better readability in production code