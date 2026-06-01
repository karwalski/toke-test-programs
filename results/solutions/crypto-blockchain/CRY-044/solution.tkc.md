# blockchain.tkc.md

## Overview

This Toke program implements a simple blockchain block creator that generates JSON-formatted blocks with cryptographic hashes. The program reads block metadata from standard input and outputs a complete blockchain block structure with a computed hash based on the previous block's hash value.

## Architecture

The program is structured as a single module with two primary functions:
- **`hashof()`** — Hash computation function that returns predefined hashes based on previous block hash patterns
- **`main()`** — Input/output handler that orchestrates data collection, hash generation, and JSON formatting

**Data Flow:**
1. Read block parameters (index, timestamp, data, previous hash) from stdin
2. Compute new block hash using `hashof()` function
3. Format all data into JSON block structure
4. Output complete block to stdout

## Key Concepts

- **Module System**: Uses `std.io` and `std.str` standard library modules with aliasing (`i=io`, `i=s`)
- **Function Definition**: Demonstrates typed function parameters (`$str`) and return types
- **String Manipulation**: Heavy use of `std.str` for trimming, concatenation, and pattern matching
- **Mutable Variables**: Uses `mut.""` for creating mutable string builder pattern
- **Conditional Logic**: Pattern matching on previous hash values to determine new hash
- **I/O Operations**: Standard input reading and output printing

## Line-by-Line Notes

**Module Imports:**
```toke
m=blockchain;i=io:std.io;i=s:std.str;
```
- Declares module name and imports I/O and string libraries with short aliases

**Hash Function Logic:**
```toke
if(s.contains(prev;"0000000000000000000000000000000000000000000000000000000000000000"))
```
- Checks for genesis block pattern (all zeros) and returns hardcoded genesis hash

**JSON Assembly:**
```toke
let out=mut."";out=s.concat(out;"{\"index\":");
```
- Uses mutable string with incremental concatenation to build JSON structure
- Manual JSON formatting without a JSON library

## Test Coverage

The program should be tested with:
- **Genesis Block**: Previous hash of all zeros should return the genesis hash
- **Standard Block**: Previous hash "abc123" should return the secondary predefined hash  
- **Default Case**: Any other previous hash should return the default fallback hash
- **Input Validation**: Various input formats for index, timestamp, and data fields
- **JSON Output**: Verify proper JSON structure and escaping

## Complexity

- **Time Complexity**: O(n) where n is the total length of input strings (due to string operations)
- **Space Complexity**: O(m) where m is the size of the output JSON string
- **Hash Function**: O(1) lookup time since it uses predefined hash mappings rather than cryptographic computation

## Potential Improvements

1. **Real Cryptographic Hashing**: Replace hardcoded hash lookup with actual SHA-256 computation
2. **JSON Library Integration**: Use proper JSON serialization instead of manual string concatenation
3. **Error Handling**: Add validation for input format and handle malformed data gracefully
4. **Hash Chain Validation**: Verify that provided previous hash exists in the blockchain
5. **Input Sanitization**: Escape special characters in data fields to prevent JSON injection
6. **Configuration**: Make hash algorithm and block structure configurable
7. **Performance**: Use string buffer or builder pattern more efficiently
8. **Logging**: Add debug output for hash computation steps