# systemdstatus.tkc.md

## Overview

This Toke program simulates a systemd service status checker that reads service unit names from standard input and returns their mock status information. The program provides hardcoded status responses for common system services like SSH, cron, and systemd-journald, defaulting to "not-found" for unrecognized services.

## Architecture

The program consists of two main functions:
- **`lookup(unit:$str):$str`** — Core lookup function that maps service names to status strings
- **`main():$i64`** — Entry point that handles I/O processing and output formatting

**Data Flow:**
1. Read service names line-by-line from stdin
2. Trim whitespace and lookup status for each service
3. Format results as "service: status" pairs
4. Output consolidated results to stdout

**Module Dependencies:**
- `std.io` — Standard I/O operations
- `std.str` — String manipulation utilities

## Key Concepts

**Toke Language Features Demonstrated:**
- **Module imports** with aliasing (`i=io:std.io`, `i=s:std.str`)
- **Function definitions** with typed parameters and return values
- **Conditional logic** using `if` statements without explicit `else`
- **Early returns** using `<` syntax
- **Mutable variables** with `mut` keyword
- **Infinite loops** with `lp(1=1)` and `br` for breaking
- **String operations** (concatenation, trimming, length checking)

## Line-by-Line Notes

```toke
m=systemdstatus  # Module declaration
```

```toke
f=lookup(unit:$str):$str{
  if(s.contains(unit;"ssh.service")){<"active sub=running pid=579"};
  if(s.contains(unit;"cron.service")){<"active sub=running pid=391"};  
  if(s.contains(unit;"systemd-journald.service")){<"active sub=running pid=127"};
  <"not-found sub=dead pid=-"  # Default fallback case
}
```

```toke
f=main():$i64{
  let out=mut."";           # Accumulator for final output
  let first=mut.1;          # Flag to handle newline formatting
  lp(1=1){                  # Infinite loop for reading input
    let line=io.readln();
    let trimmed=s.trim(line);
    if(s.len(trimmed)=0){br}; # Break on empty line
    let status=lookup(trimmed);
    if(first=1){first=0}el{out=s.concat(out;"\n")}; # Add newlines between entries
    out=s.concat(out;s.concat(trimmed;s.concat(": ";status))); # Format: "service: status"
  };
  io.println(out);
  <0  # Return success code
}
```

## Test Coverage

**Recommended test cases should verify:**
- **Known services:** Input "ssh.service", "cron.service", "systemd-journald.service" 
- **Unknown services:** Input arbitrary service names
- **Empty input:** Single newline should terminate gracefully
- **Multiple services:** Batch processing with proper newline formatting
- **Whitespace handling:** Services with leading/trailing spaces
- **Output format:** Correct "service: status" formatting

## Complexity

**Time Complexity:** O(n×m) where n = number of input lines, m = average service name length (due to string contains operations)

**Space Complexity:** O(k) where k = total length of output string (accumulated in `out` variable)

## Potential Improvements

1. **Data Structure Optimization:** Replace linear string searching with hash map lookup for O(1) service resolution
2. **Real Integration:** Connect to actual systemctl commands via system calls
3. **Error Handling:** Add validation for malformed input and I/O error management
4. **Configuration:** External service database instead of hardcoded values
5. **Output Streaming:** Process and output results incrementally instead of accumulating
6. **Service Discovery:** Auto-detect available services from system
7. **Rich Status Info:** Include additional fields like memory usage, uptime, and dependencies