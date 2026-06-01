# Chat Message Formatter - Documentation

**File:** `chat_formatter.tkc.md`

## Overview

This Toke program parses JSON-formatted chat messages and formats them into a human-readable chat log display. It processes stdin input containing chat message JSON objects and outputs a formatted conversation view with timestamps, sender names, and message content, distinguishing between the current user's messages (prefixed with `>`) and others' messages (prefixed with `<`).

## Architecture

The program follows a functional decomposition pattern with four main components:

- **Data Extraction Layer** (`extract`) - Parses JSON-like key-value pairs from input strings
- **Time Processing** (`fmttime`) - Converts ISO timestamp strings to HH:MM format  
- **Message Formatting** (`formatmsg`) - Combines extracted data into readable chat format
- **Main Controller** (`main`) - Orchestrates input processing and output generation

**Data Flow:**
```
stdin → main() → formatmsg() → [extract(), fmttime()] → formatted output
```

## Key Concepts

- **String Manipulation**: Heavy use of `std.str` module for splitting, slicing, and concatenation
- **Mutable Variables**: `mut.""` and `mut.1` for building output strings and state tracking
- **Conditional Logic**: Pattern matching with `if/el` constructs
- **Loop Control**: `lp(1=1)` infinite loop with `br` break condition
- **I/O Operations**: `std.io` for reading lines and printing results
- **Manual JSON Parsing**: Custom string parsing instead of dedicated JSON library

## Line-by-Line Notes

**Module Imports & Aliases:**
```toke
m=chat;i=io:std.io;i=s:std.str;
```
- Creates short aliases for frequently used modules

**Extract Function:**
```toke
let parts=s.split(line;key);if(parts.len()>=2){let rest=parts.get(1);let q=s.split(rest;"\"")...
```
- Splits on key, then extracts quoted value after the key
- Returns empty string if parsing fails

**Time Formatter:**
```toke
if(s.contains(ts;"T")){let parts=s.split(ts;"T")...let hm=s.slice(tpart;0;5)
```
- Assumes ISO 8601 format (YYYY-MM-DDTHH:MM:SS)
- Extracts only HH:MM portion for display

**Message Builder:**
```toke
if(sender=me){out=s.concat(out;"> ")}el{out=s.concat(out;"< ")};
```
- Distinguishes user's messages with `>` prefix vs others with `<`

**Main Loop:**
```toke
if(first=1){result=s.concat(result;formatted);first=0}el{result=s.concat(result;"\n")...
```
- Tracks first message to avoid leading newline in output

## Test Coverage

To verify this program, test cases should include:

- **Valid JSON messages** with all required fields (sender, timestamp, text)
- **Missing fields** to test graceful degradation  
- **Malformed timestamps** (no T separator, short format)
- **Empty input** (immediate EOF)
- **User vs other sender** scenarios
- **Special characters** in message text and sender names
- **Multiple messages** to verify newline handling

## Complexity

- **Time Complexity**: O(n × m) where n = number of messages, m = average message length
- **Space Complexity**: O(k) where k = total output size (all messages concatenated)
- **Performance Bottleneck**: String concatenation in loop creates intermediate strings

## Potential Improvements

1. **JSON Library Integration**: Replace manual parsing with proper JSON deserializer for robustness
2. **Error Handling**: Add explicit error messages for malformed input instead of silent fallbacks
3. **String Builder**: Use array accumulation + join instead of repeated concatenation for better performance
4. **Timestamp Flexibility**: Support multiple timestamp formats (Unix, relative times)
5. **Configuration**: Make message prefixes (`>`, `<`) and format strings configurable
6. **Streaming Output**: Print messages as processed instead of buffering entire result
7. **Input Validation**: Verify JSON structure before attempting field extraction
8. **Unicode Support**: Ensure proper handling of non-ASCII characters in messages