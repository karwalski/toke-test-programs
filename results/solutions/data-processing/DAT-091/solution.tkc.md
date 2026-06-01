# expandcidr.tkc.md

## Overview

This toke program expands a CIDR (Classless Inter-Domain Routing) notation into all possible IP addresses within that subnet. It reads a CIDR block from standard input (e.g., "192.168.1.0/24") and outputs each individual IP address in the range on separate lines.

## Architecture

The program follows a linear procedural structure within a single `main()` function:

1. **Input Processing** — Parse CIDR notation from stdin
2. **IP Conversion** — Convert dotted decimal to 32-bit integer representation  
3. **Network Calculation** — Determine network base and host count
4. **Address Generation** — Iterate through all possible host addresses
5. **Output Formatting** — Convert back to dotted decimal and print

**Modules Used:**
- `std.io` — Standard I/O operations
- `std.str` — String manipulation and parsing

## Key Concepts

- **String Processing** — Extensive use of `split()`, `trim()`, `concat()` for parsing
- **Type Conversion** — `toint()` and `fromint()` for string/integer conversion
- **Mutable Variables** — `mut` keyword for loop counters and accumulating values
- **Loop Constructs** — `lp()` syntax for iterative operations
- **Integer Arithmetic** — Bit manipulation through division/multiplication for network masks

## Line-by-Line Notes

**Input Parsing:**
```toke
let parts=s.split(line;"/")  // Split "192.168.1.0/24" into IP and prefix
let n=s.toint(prefix)        // Convert "/24" to integer 24
```

**IP to Integer Conversion:**
```toke
let baseval=b0*16777216+b1*65536+b2*256+b3  // Convert to 32-bit integer
```
Uses powers of 256 (2^8, 2^16, 2^24) to pack octets into single integer.

**Host Count Calculation:**
```toke
let hostbits=32-n           // /24 network = 8 host bits
lp(let k=0;k<hostbits;k=k+1){count=count*2}  // count = 2^hostbits
```

**Network Base Calculation:**
```toke
let netbase=(baseval/divisor)*divisor  // Zero out host bits via integer division
```

**Integer to IP Conversion:**
```toke
let o0=cur/16777216         // Extract highest octet
let r0=cur-o0*16777216      // Remainder for next octets
```

## Test Coverage

To verify correctness, test cases should include:

- **Small subnets** — `/30` (4 addresses), `/29` (8 addresses)
- **Common networks** — `/24` (256 addresses), `/16` (65536 addresses)  
- **Edge cases** — `/32` (single host), `/0` (entire IPv4 space, may be impractical)
- **Various IP ranges** — Private (192.168.x.x, 10.x.x.x) and public addresses

## Complexity

- **Time Complexity:** O(2^(32-n)) where n is the CIDR prefix length
- **Space Complexity:** O(1) — constant memory usage regardless of subnet size

**Performance Notes:**
- `/24` network = 256 addresses (fast)
- `/16` network = 65,536 addresses (moderate)  
- `/8` network = 16,777,216 addresses (slow)

## Potential Improvements

1. **Input Validation** — Check for malformed CIDR notation, invalid IP octets (>255)
2. **Memory Optimization** — For large subnets, consider streaming output vs. storing all addresses
3. **Error Handling** — Graceful handling of invalid input rather than runtime errors
4. **Output Formatting** — Optional JSON/CSV output formats
5. **IPv6 Support** — Extend to handle IPv6 CIDR blocks
6. **Performance** — Use bitwise operations instead of multiplication/division for powers of 2
7. **Code Structure** — Extract IP conversion logic into reusable functions
8. **Range Limits** — Warn or abort for excessively large subnets (e.g., `/8` or larger)