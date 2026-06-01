# html2md.tkc.md

## Overview

This toke program converts basic HTML markup to Markdown format by reading HTML from standard input and applying a series of string replacements. It handles common HTML elements like headers, paragraphs, bold text, and unordered lists, transforming them into their Markdown equivalents.

## Architecture

The program follows a simple linear architecture:
- **Module**: `html2md` - single-purpose HTML to Markdown converter
- **Imports**: Uses standard library modules for I/O (`std.io`) and string operations (`std.str`)
- **Main Function**: Single `main()` function that orchestrates the conversion process
- **Data Flow**: Input → Read line → Apply transformations → Output result

```
stdin → readln() → series of replace() calls → trim() → println() → stdout
```

## Key Concepts

**Toke Language Features Demonstrated:**
- **Module system**: Module declaration and standard library imports
- **Import aliasing**: `i=io:std.io` and `i=s:std.str` for namespace management
- **Mutable variables**: `let r=mut.line` creates a mutable string reference
- **Method chaining**: Sequential string transformations on the same variable
- **Standard library usage**: I/O operations and string manipulation functions
- **Return values**: Function returns `$i64` (signed 64-bit integer) with `<0` (return 0)

## Line-by-Line Notes

```toke
m=html2md;
```
- Declares module named `html2md`

```toke
i=io:std.io;i=s:std.str;
```
- Imports standard I/O library with alias `io`
- Imports standard string library with alias `s`

```toke
let line=io.readln();let r=mut.line;
```
- Reads a line from standard input
- Creates mutable copy `r` for transformation

```toke
r=s.replace(r;"<h1>";"# ");r=s.replace(r;"</h1>";"\n\n");
```
- Converts HTML h1 tags to Markdown header syntax
- Opening tag becomes `# `, closing tag becomes double newline

```toke
r=s.replace(r;"<p>";"");r=s.replace(r;"</p>";"");
```
- Removes paragraph tags (Markdown uses blank lines for paragraphs)

```toke
r=s.replace(r;"<b>";"**");r=s.replace(r;"</b>";"**");
```
- Converts bold tags to Markdown bold syntax (`**text**`)

```toke
r=s.replace(r;"<ul>";"");r=s.replace(r;"</ul>";"");
r=s.replace(r;"<li>";"- ");r=s.replace(r;"</li>";"\n");
```
- Removes ul container tags
- Converts list items to Markdown bullet points with newlines

```toke
r=s.trim(r);io.println(r);<0
```
- Trims whitespace and prints result
- Returns 0 (success exit code)

## Test Coverage

**Recommended test cases should verify:**
- Header conversion: `<h1>Title</h1>` → `# Title\n\n`
- Paragraph handling: `<p>text</p>` → `text`
- Bold formatting: `<b>bold</b>` → `**bold**`
- List conversion: `<ul><li>item</li></ul>` → `- item\n`
- Mixed HTML with multiple elements
- Edge cases: empty input, malformed HTML, nested tags

## Complexity

- **Time Complexity**: O(n×m) where n is input length and m is number of replacement operations (9 replacements)
- **Space Complexity**: O(n) for string storage and intermediate results
- **Scalability**: Limited to single-line input; each replacement scans entire string

## Potential Improvements

1. **Multi-line support**: Read entire input stream instead of single line
2. **Error handling**: Validate HTML structure and handle malformed input
3. **Performance optimization**: Use single-pass parser instead of multiple string replacements
4. **Extended HTML support**: Add support for links, images, code blocks, tables
5. **Configurable mapping**: Allow custom HTML-to-Markdown transformation rules
6. **Streaming processing**: Handle large files without loading everything into memory
7. **Proper HTML parsing**: Use DOM parser for nested and complex HTML structures
8. **Output formatting**: Better handling of whitespace and newline management