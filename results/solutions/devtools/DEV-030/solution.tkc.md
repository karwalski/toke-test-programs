# glob.tkc.md

**Companion Documentation for glob.toke**

## Overview

This program implements a simple glob pattern matcher that reads a pattern from input, then tests multiple file paths against that pattern. It supports basic wildcard matching (`*`), recursive directory matching (`**/`), and exact string matching, displaying results and a final match count summary.

## Architecture

The program is structured as a single module with three main functions:

- **`endswith()`** — String suffix checking utility
- **`matchglob()`** — Core pattern matching logic with three matching modes
- **`main()`** — Interactive loop for reading pattern and paths, coordinating matching and output

**Data Flow:**
1. Read glob pattern from stdin
2. Enter loop reading file paths until empty line
3. Each path is processed through `matchglob()` → `endswith()` chain
4. Results accumulated and displayed with final statistics

## Key Concepts

**Toke Language Features Demonstrated:**
- **Type System**: Explicit type annotations (`$str`, `$bool`, `$i64`)
- **String Library**: Extensive use of `std.str` for manipulation (`len`, `slice`, `contains`, `trim`)
- **Mutable Variables**: `mut` keyword for counters that change during execution
- **Control Flow**: `if/el` conditionals and `lp()` loops
- **Module Imports**: Aliased imports (`io:std.io`, `s:std.str`)
- **Early Returns**: `<expression` syntax for function returns

## Line-by-Line Notes

**Lines 1-2**: Module imports with short aliases for cleaner code
```toke
m=glob;i=io:std.io;i=s:std.str;
```

**`endswith()` function**: Manual suffix checking since no built-in exists
```toke
let tail=s.slice(path;pl-sl;pl)  // Extract last 'suf.length' characters
```

**`matchglob()` pattern matching hierarchy**:
1. `**/` pattern: Recursive directory match, extracts extension after `**/`
2. `*` pattern: Single-level wildcard, rejects paths with `/` (directories)
3. Fallback: Exact string comparison

**Main loop termination**:
```toke
if(s.len(line)<1){done=1}  // Empty line signals end of input
```

## Test Coverage

The program handles three distinct matching scenarios:
- **Recursive patterns** (`**/*.txt`): Matches any `.txt` file at any directory depth
- **Simple wildcards** (`*.js`): Matches extensions in current directory only
- **Exact matches** (`config.json`): Literal string comparison

**Edge Cases Covered:**
- Empty input lines (terminates gracefully)
- Suffix longer than path string
- Paths containing directory separators vs. simple filenames

## Complexity

**Time Complexity:** O(n × m) where n = number of input paths, m = average path length
**Space Complexity:** O(m) for string operations and temporary variables

**Performance Notes:**
- Multiple string operations per match (slice, contains, len)
- Linear scan for pattern detection in each path

## Potential Improvements

1. **Pattern Compilation**: Pre-parse pattern once instead of re-analyzing for each path
2. **Enhanced Glob Support**: Add character classes `[abc]`, question mark `?`, brace expansion `{a,b}`
3. **Error Handling**: Validate pattern syntax and handle malformed input gracefully
4. **Memory Optimization**: Reduce temporary string allocations in hot matching loop
5. **Regex Backend**: Consider regex engine for more sophisticated pattern matching
6. **Batch Processing**: Accept file list as command line argument instead of interactive mode
7. **Case Sensitivity**: Add option for case-insensitive matching on different filesystems