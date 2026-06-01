# extractheadings.tkc.md

## Overview

This Toke program parses Markdown-style heading lines from standard input and converts them into a structured format. It reads lines containing hash symbols (`#`) as heading markers and outputs them in the format `H{level}: {text}` where level indicates the heading depth.

## Architecture

The program consists of two main functions with a simple pipeline architecture:

- **`extractheadings(line: $str): $str`** — Core parsing function that processes individual lines
- **`main(): $i64`** — I/O coordinator that reads input, processes each line, and outputs results
- **Module imports** — Standard library dependencies for I/O and string manipulation

Data flows linearly: stdin → line processing → heading extraction → formatted output → stdout.

## Key Concepts

**Toke Language Features Demonstrated:**
- **Module system**: Import aliasing (`i=io:std.io`, `i=s:std.str`)
- **Mutable variables**: `mut` keyword for stateful counters and accumulators
- **String manipulation**: Extensive use of `slice()`, `concat()`, `len()`, `trim()`
- **Control flow**: `if`/`else` conditionals and `lp()` loops
- **Type annotations**: Explicit `$str` and `$i64` return types
- **Early returns**: Using `<value` syntax for function exits

## Line-by-Line Notes

**Header Detection Logic:**
```toke
let firstchar=s.slice(line;0;1);if(firstchar="#"){isheader=true;
```
Checks if line starts with `#` to identify potential headings.

**Level Counting Loop:**
```toke
lp(k<s.len(line)){let ch=s.slice(line;k;k+1);if(ch="#"){headerlevel=headerlevel+1;k=k+1}el{k=s.len(line)}}
```
Counts consecutive `#` characters to determine heading depth. Loop terminates early when non-`#` character found.

**Text Extraction:**
```toke
let headingtext=s.slice(line;headerlevel+1;s.len(line));
```
Extracts heading text by skipping past hash symbols and the following space.

**Accumulation Pattern:**
```toke
if(s.len(result)>0){result=s.concat(result;"\n")};
```
Adds newlines between multiple headings while avoiding leading newline.

## Test Coverage

**Recommended test cases should verify:**
- Single-level headings (`# Title` → `H1: Title`)
- Multi-level headings (`### Deep` → `H3: Deep`)
- Mixed content (headings + non-heading lines)
- Empty input handling
- Whitespace trimming behavior
- Edge cases: lines with only `#` symbols

## Complexity

- **Time Complexity**: O(n×m) where n = number of input lines, m = average line length
- **Space Complexity**: O(k) where k = total length of extracted headings
- **Bottleneck**: String concatenation in result accumulation could be optimized

## Potential Improvements

1. **Performance**: Use string builder pattern instead of repeated concatenation
2. **Robustness**: Add validation for malformed headings (e.g., `#heading` without space)
3. **Flexibility**: Support alternative heading syntaxes (Setext-style underlines)
4. **Error handling**: Graceful handling of I/O errors
5. **Code structure**: Extract level counting into separate function for better readability
6. **Memory efficiency**: Stream processing instead of accumulating full result string