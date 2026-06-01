# Toke Event Log Processor Documentation (.tkc.md)

## Overview

This program processes blockchain event commands from standard input and converts them into a structured JSON format. It maps event names (Transfer, Mint, Approval, Burn) to their corresponding Ethereum-style topic hashes and formats the output as a JSON array of event objects.

## Architecture

The program consists of two main functions:
- **`topicfor(name: $str): $str`** — Maps event names to their hexadecimal topic hashes
- **`main(): $i64`** — Handles input parsing, JSON construction, and output formatting

**Data Flow:**
1. Read definition line (ignored)
2. Process EMIT commands line-by-line
3. Extract event name and parameters
4. Map event name to topic hash
5. Build JSON structure incrementally
6. Output final JSON array

**Dependencies:**
- `std.io` for input/output operations
- `std.str` for string manipulation

## Key Concepts

**Toke Language Features Demonstrated:**
- **Type annotations**: `$str`, `$i64` for explicit typing
- **Mutable variables**: `mut.` prefix for variables that change
- **String concatenation**: `s.concat()` for building output
- **Array operations**: `.get()`, `.len()` for string array access
- **Control flow**: `if` statements and `lp` (loop) constructs
- **Module imports**: Aliased imports (`i=io:std.io`)

## Line-by-Line Notes

**Lines 1-2**: Module imports with aliases (`ctr`, `io:std.io`, `s:std.str`)

**`topicfor` function**: 
- Maps standard ERC-20/blockchain event names to their keccak256 topic hashes
- Uses early returns (`<"hash"`) for each event type
- Returns empty string for unknown events

**`main` function initialization**:
- `defline=io.readln()`: Reads and discards first line
- `out=mut."["`: Starts JSON array construction
- `count=mut.0`: Tracks number of events for comma placement

**Main processing loop**:
- `lp(s.len(line)>0)`: Continues while input lines exist
- `s.split(trimmed;" ")`: Splits command line on spaces
- **EMIT command handling**: Extracts event name and parameters
- **JSON construction**: Builds `{"topic":"hash","data":["param1","param2"]}` format
- **Comma management**: Adds commas between array elements when `count>0`

## Test Coverage

To verify this program, test cases should include:

1. **Valid EMIT commands**: `EMIT Transfer 0x123 0x456 1000`
2. **Multiple events**: Sequential EMIT commands
3. **Unknown event names**: Events not in the topic mapping
4. **Empty parameter lists**: `EMIT Approval`
5. **Edge cases**: Empty lines, malformed commands
6. **Single vs multiple events**: JSON comma handling

## Complexity

**Time Complexity**: O(n×m) where n = number of input lines, m = average line length
- String operations dominate performance
- Each line requires splitting and multiple concatenations

**Space Complexity**: O(k) where k = total output JSON size
- Builds entire output string in memory
- Input processing is line-by-line (streaming)

## Potential Improvements

1. **Error Handling**: Add validation for malformed EMIT commands and invalid parameters

2. **Performance Optimization**: 
   - Use string builder pattern instead of repeated concatenation
   - Pre-allocate output buffer based on input size estimation

3. **Code Structure**:
   - Extract JSON building into separate functions
   - Add input validation and error reporting
   - Use constants for topic hashes instead of string literals

4. **Extensibility**:
   - Load topic mappings from external configuration
   - Support additional event types beyond the current four
   - Add data type validation for event parameters

5. **Output Format**: 
   - Add pretty-printing option for JSON output
   - Include metadata like event count or processing timestamp

6. **Memory Efficiency**: Stream JSON output instead of building complete string in memory for large inputs