# Queue Operation Simulator - Companion Documentation

## Overview

This Toke program simulates a message queue system that processes JSON-formatted operation records. It parses enqueue, dequeue, acknowledge, crash, and recover operations to demonstrate queue state management with in-flight message tracking and fault tolerance.

## Architecture

The program consists of three main functions:

- **`parseop()`** - Extracts operation type from JSON segments using nested string matching
- **`parsemsg()`** - Extracts message content from JSON by splitting on specific delimiters  
- **`main()`** - Orchestrates the simulation by parsing input, maintaining queue state, and generating output

**Data Flow:**
1. Read JSON array from stdin
2. Split into individual operation records
3. For each record: parse operation → update state → append to output
4. Print final accumulated output

**State Variables:**
- `size` - Current queue length
- `inflight` - Count of dequeued but unacknowledged messages
- `firstmsg` - Next message to be dequeued (FIFO simulation)

## Key Concepts

- **Mutable Variables** - Extensive use of `mut.` for state tracking
- **String Manipulation** - Heavy reliance on `std.str` for parsing and output formatting
- **Conditional Chaining** - Nested if-else structures for operation dispatch
- **Type System** - Function signatures with explicit parameter and return types (`$str`, `$i64`)
- **Standard Library** - Integration with `std.io` and `std.str` modules

## Line-by-Line Notes

**Lines 1-3:** Module imports using aliasing (`m=queue`, `i=io:std.io`, `i=str:std.str`)

**Lines 4-10:** `parseop()` uses cascading string contains checks rather than pattern matching

**Lines 11-18:** `parsemsg()` implements manual JSON parsing by splitting on `"msg":"` and extracting content before next quote

**Lines 21-22:** Input preprocessing removes array brackets and splits on `},{` to separate records

**Lines 29-31:** FIFO queue simulation - only tracks first message since it assumes FIFO behavior

**Lines 45-58:** Crash/recover logic manages in-flight message restoration to queue

**Lines 61-63:** Output post-processing removes trailing newline before printing

## Test Coverage

The program handles these operation scenarios:

- **Enqueue** - Adds messages and tracks queue size
- **Dequeue from empty queue** - Returns "EMPTY" status
- **Dequeue with messages** - Returns FIFO message, marks as in-flight
- **Acknowledge** - Confirms message processing, reduces in-flight count
- **Crash with/without in-flight** - Simulates message loss
- **Recover with/without unacked** - Restores lost messages to queue

## Complexity

- **Time Complexity:** O(n×m) where n = number of operations, m = average string length (due to string concatenation)
- **Space Complexity:** O(k) where k = total output length (grows with each operation)

## Potential Improvements

1. **Performance** - Replace string concatenation with string builder or array joining
2. **JSON Parsing** - Use proper JSON parser instead of manual string splitting
3. **Queue Implementation** - Use actual queue data structure instead of single `firstmsg` variable
4. **Error Handling** - Add validation for malformed JSON and edge cases
5. **Pattern Matching** - Replace nested if-else with pattern matching if available
6. **Memory Efficiency** - Process operations in streaming fashion rather than accumulating full output
7. **Type Safety** - Add bounds checking for array access operations