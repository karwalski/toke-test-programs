# SSRF Risk Classifier Documentation

**File:** `ssrf.tkc.md`

## Overview

This Toke program implements a basic Server-Side Request Forgery (SSRF) vulnerability detector that analyzes input lines for potentially dangerous URL parameters. The program reads a single line of input and classifies it as either "POTENTIAL_SSRF" or "SAFE" based on the presence of URL parameter patterns.

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Input Line    │───▶│  classifyrisk()  │───▶│  Risk Rating    │
│  (from stdin)   │    │   (classifier)   │    │ (SAFE/SSRF)     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │  String Pattern  │
                       │    Matching      │
                       └──────────────────┘
```

### Modules
- **ssrf** - Main module containing the SSRF detection logic
- **std.io** - Standard I/O operations (aliased as `io`)
- **std.str** - String manipulation utilities (aliased as `s`)

### Functions
- `classifyrisk(line: $str): $str` - Core classification logic
- `main(): $i64` - Entry point and I/O orchestration

## Key Concepts

### Toke Language Features Demonstrated
- **Module system**: Import and aliasing (`m=ssrf`, `i=io:std.io`)
- **Type annotations**: Explicit parameter and return types (`$str`, `$i64`)
- **String operations**: Pattern matching using `std.str.contains()`
- **Control flow**: Conditional branching with early returns
- **I/O handling**: Standard input/output operations
- **Return syntax**: Toke's `<` return operator

### Security Pattern Detection
- **URL parameter detection**: Looks for `url=` patterns
- **URL encoding awareness**: Detects URL-encoded parameters (`url%3D`)

## Line-by-Line Notes

```toke
m=ssrf;
```
Module declaration - defines the current module as "ssrf"

```toke
i=io:std.io;i=s:std.str;
```
Import aliases - `io` for standard I/O operations, `s` for string utilities

```toke
f=classifyrisk(line:$str):$str{
```
Function definition with explicit typing - takes string input, returns classification string

```toke
if(s.contains(line;"url=")){<"POTENTIAL_SSRF"};
if(s.contains(line;"url%3D")){<"POTENTIAL_SSRF"};
```
Pattern matching logic - checks for both plain and URL-encoded "url=" parameters using early returns

```toke
<"SAFE"
```
Default return value when no suspicious patterns are found

```toke
let line=io.readln();let risk=classifyrisk(line);
```
Input processing pipeline - read line, classify risk level

## Test Coverage

### Positive Cases (Should detect SSRF)
- Lines containing `url=` parameter
- Lines containing URL-encoded `url%3D` parameter
- Mixed case and embedded contexts

### Negative Cases (Should return SAFE)
- Plain text without URL parameters
- Other parameter names (`uri=`, `link=`, etc.)
- Partial matches (`urla=`, `curl=`)

### Example Test Cases
```bash
echo "GET /api?url=http://evil.com" | ./ssrf     # → POTENTIAL_SSRF
echo "POST data=url%3Dhttp://evil.com" | ./ssrf  # → POTENTIAL_SSRF
echo "GET /api?id=123" | ./ssrf                  # → SAFE
```

## Complexity

- **Time Complexity**: O(n) where n is the length of the input line (due to string contains operations)
- **Space Complexity**: O(1) - constant memory usage regardless of input size
- **I/O Complexity**: Single read operation, single write operation

## Potential Improvements

### Security Enhancements
1. **Case-insensitive matching** - Add `s.tolower()` for better detection
2. **Extended pattern library** - Include `uri=`, `redirect=`, `callback=` parameters
3. **Regex support** - More sophisticated pattern matching for complex encodings
4. **Multiple encoding detection** - Handle double encoding, hex encoding

### Code Quality
1. **Error handling** - Handle I/O errors and malformed input gracefully
2. **Configuration** - External pattern configuration file
3. **Logging** - Add structured logging for audit trails
4. **Batch processing** - Process multiple lines or files

### Performance
1. **Compiled patterns** - Pre-compile regex patterns for repeated use
2. **Streaming processing** - Handle large files without loading into memory
3. **Parallel processing** - Multi-threaded analysis for bulk data

### Example Enhanced Version
```toke
// Improved pattern matching
patterns = ["url=", "uri=", "redirect=", "callback="];
encodedPatterns = ["url%3D", "uri%3D", "redirect%3D"];
```