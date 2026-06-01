# diffstat.tkc.md

## Overview

This Toke program implements a diff statistics analyzer that reads unified diff input from stdin and produces a summary report showing the number of added and deleted lines per file. It mimics the behavior of the Unix `diffstat` utility by parsing diff format and outputting insertion/deletion counts with proper grammatical formatting.

## Architecture

The program consists of a single `main()` function with a linear processing pipeline:

1. **Input Collection** — Read all stdin lines into a concatenated string
2. **Diff Parsing** — Split input and extract filename from `+++` headers  
3. **Line Analysis** — Count `+` (additions) and `-` (deletions) while filtering metadata
4. **Output Formatting** — Generate summary with proper singular/plural grammar

**Dependencies:**
- `std.io` — Terminal I/O operations
- `std.str` — String manipulation and parsing

## Key Concepts

**Toke Language Features Demonstrated:**
- **Mutable Variables** — `mut` keyword for stateful counters and flags
- **String Operations** — Extensive use of `concat()`, `slice()`, `split()`, and `len()`
- **Control Flow** — `lp()` loops for input processing and array iteration
- **Type Conversion** — `fromint()` for numeric-to-string formatting
- **Standard Library** — Heavy reliance on `std.str` and `std.io` modules

## Line-by-Line Notes

**Input Processing:**
```toke
let diff=mut."";let first=mut.true;let line=mut.io.readln();
lp(s.len(line)>0){if(first){diff=line;first=false}el{diff=s.concat(s.concat(diff;"\n");line)};line=io.readln()}
```
Uses a `first` flag to avoid leading newline when concatenating input lines.

**Filename Extraction:**
```toke
if(s.len(ln)>=4){let p4=s.slice(ln;0;4);if(p4="+++ "){fname=s.slice(ln;6;s.len(ln))}}
```
Parses `+++ filename` headers, skipping the prefix to extract the actual filename.

**Addition/Deletion Filtering:**
```toke
if(c="+"){if(s.len(ln)>=3){let p3=s.slice(ln;0;3);if(p3="+++"){}el{adds=adds+1}}el{adds=adds+1}}
```
Counts `+` lines but excludes `+++` metadata headers through nested conditionals.

**Grammar Handling:**
```toke
let insword=mut."insertions(+)";if(adds=1){insword="insertion(+)"}
```
Dynamically adjusts singular vs. plural forms based on count values.

## Test Coverage

**Recommended test cases should verify:**
- Single-file diffs with mixed additions/deletions
- Multiple-file diffs with proper filename extraction
- Edge cases: zero changes, single-line changes
- Grammar correctness for singular counts (1 insertion, 1 deletion)
- Proper filtering of diff metadata (`+++`, `---`, `@@` lines)
- Empty input and malformed diff handling

## Complexity

**Time Complexity:** O(n) where n is the total number of input characters
- Single pass through stdin for collection
- Single pass through parsed lines for analysis

**Space Complexity:** O(n) for storing the entire diff content in memory
- Could be optimized to O(1) with streaming line-by-line processing

## Potential Improvements

1. **Memory Optimization** — Process lines incrementally instead of loading entire diff
2. **Multi-file Support** — Track statistics per file and provide aggregate summary
3. **Error Handling** — Validate diff format and handle malformed input gracefully
4. **Enhanced Parsing** — Support context lines, binary files, and rename detection
5. **Code Structure** — Extract parsing logic into separate functions for readability
6. **Output Formats** — Add options for JSON, CSV, or custom formatting
7. **Performance** — Reduce string concatenation overhead with StringBuilder pattern