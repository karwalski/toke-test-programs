# disappearingmsg.tkc.md

## Overview

This Toke program processes disappearing messages by parsing a custom JSON format to determine message visibility status. It calculates whether messages have expired based on their read timestamps and time-to-live (TTL) values, displaying the current status and timing information for each message.

## Architecture

The program is structured as a single module with four main functions:
- **`parsetime()`** — Converts ISO datetime strings to epoch seconds
- **`pad()`** — Zero-pads single digits for time formatting  
- **`fmthms()`** — Formats epoch seconds into HH:MM:SS format
- **`main()`** — Orchestrates input parsing and message status evaluation

Data flows from standard input (current time + JSON) through string parsing utilities to produce formatted status output for each message.

## Key Concepts

- **String manipulation** — Heavy use of `std.str` for slicing, splitting, and concatenation
- **Type conversion** — Converting between strings and integers using `s.toint()` and `s.fromint()`
- **Mutable variables** — Loop counter using `mut` keyword
- **Control flow** — Conditional logic with `if/el` and `lp()` loop construct
- **Manual JSON parsing** — String-based parsing instead of structured JSON library

## Line-by-Line Notes

**Lines 1-7**: Module imports and time parsing setup. The `parsetime()` function implements a simplified date calculation (365 days/year, 31 days/month) rather than precise calendar math.

**Lines 8-10**: Helper functions for formatting. `pad()` ensures two-digit display, `fmthms()` converts total seconds to readable time format.

**Lines 11-13**: Input processing. Expects current timestamp on first line, JSON array on second line with bracket removal.

**Lines 14-20**: Message parsing loop. Manually extracts JSON fields using string splitting on known patterns like `"text":"` and `"ttl_after_read_seconds":`.

**Lines 21-30**: Status determination logic. Checks if message was read (`null` vs timestamp), calculates expiration time, and determines current visibility state with appropriate messaging.

## Test Coverage

To thoroughly test this program, verify:
- **Time parsing accuracy** with various ISO datetime formats
- **JSON parsing robustness** with different field orders and values  
- **Expiration logic** for unread, active, and expired messages
- **Edge cases** like zero TTL, malformed timestamps, empty message lists
- **Output formatting** consistency across all status types

## Complexity

- **Time Complexity**: O(n×m) where n = number of messages, m = average string operations per message
- **Space Complexity**: O(k) where k = total length of input strings (creates multiple substring copies)

The string-heavy parsing approach creates significant temporary allocations during split operations.

## Potential Improvements

1. **Accurate date calculation** — Replace approximate day counting with proper calendar arithmetic
2. **Structured JSON parsing** — Use a proper JSON library to improve reliability and reduce string manipulation overhead
3. **Error handling** — Add validation for malformed timestamps, missing JSON fields, and invalid numeric conversions
4. **Memory optimization** — Reduce string copying by using string views or streaming parsing
5. **Time zone support** — Handle timezone information in timestamps for global usage
6. **Configuration** — Make date/time format configurable rather than hardcoded
7. **Performance** — Cache parsed timestamps and optimize string operations for large message volumes