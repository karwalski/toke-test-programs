# Schedule Generator - Companion Documentation (.tkc.md)

## Overview

This Toke program generates a study schedule by processing user input or JSON data containing academic topics. The program creates formatted schedule entries with dates and time allocations for subjects like Physics, Chemistry, Math, Science, and History.

## Architecture

The program consists of two main functions:
- **`parsejson`** — Parses JSON input to extract topic arrays and generates schedules for science subjects
- **`main`** — Handles user input via readline, with fallback to default topic scheduling

**Data Flow:**
1. Main reads user input line
2. Checks for Physics/Chemistry keywords in input
3. Either outputs science schedules directly or processes default topic array
4. Uses string manipulation utilities for formatting output

## Key Concepts

**Toke Language Features Demonstrated:**
- **Module imports:** `schedule`, `std.io`, `std.str` 
- **Mutable variables:** `mut` keyword for loop counters and state tracking
- **Array literals:** `@()` syntax for topic and date collections
- **String operations:** Slicing, concatenation, trimming, splitting
- **Control flow:** `lp` (loop), `if/el` conditionals, `br` (break)
- **Type annotations:** Function signatures with `$str`, `$void`, `$i64`

## Line-by-Line Notes

**JSON Parser Function:**
- **Line 1:** Searches for "topics" substring to locate JSON topic array
- **Lines 2-8:** Manual JSON bracket matching to find array boundaries `[...]`
- **Lines 9-12:** Extracts and splits comma-separated topics
- **Lines 13-15:** Filters for science subjects and formats output with string concatenation

**Main Function:**
- **Line 17:** Direct pattern matching for science subjects in user input
- **Lines 19-21:** Fallback arrays for topics, hours, and dates
- **Lines 22-26:** Parallel iteration through dates/topics with bounds checking

## Test Coverage

**Input Scenarios:**
- ✅ User input containing "Physics" or "Chemistry" keywords
- ✅ JSON input with topics array (science subject filtering)
- ✅ Default scheduling for Math/Science/History topics
- ✅ String formatting with date, topic, and hour interpolation

**Edge Cases:**
- Topic trimming and quote removal in JSON parsing
- Array bounds checking in parallel iteration
- Empty topic filtering

## Complexity

**Time Complexity:** O(n) where n is input string length for JSON parsing, O(m) for topic array processing
**Space Complexity:** O(k) where k is number of topics stored in arrays

The JSON parser performs linear string scanning, while the main scheduling logic has constant-time array operations.

## Potential Improvements

1. **JSON Parsing:** Replace manual bracket matching with proper JSON library usage
2. **Error Handling:** Add validation for malformed JSON and empty inputs
3. **Configuration:** Extract hardcoded dates/hours into configurable parameters
4. **Output Format:** Support multiple output formats (CSV, XML, etc.)
5. **Topic Validation:** Implement topic category validation and scheduling rules
6. **Code Structure:** Separate parsing, scheduling, and formatting into distinct modules
7. **Performance:** Use StringBuilder pattern for complex string concatenations