# blackjack.tkc.md

## Overview

This toke program implements a blackjack hand evaluator that calculates the optimal total value of a given hand of cards. The program reads a space-separated list of cards from standard input and outputs whether the hand busts (exceeds 21) or is safe, along with the calculated total.

## Architecture

```
blackjack module
├── evaluate(hand: $str): $i64
│   ├── Card parsing and value assignment
│   ├── Initial total calculation
│   └── Ace optimization logic
└── main(): $i64
    ├── Input handling
    ├── Hand evaluation
    └── Output formatting
```

**Data Flow:**
1. `main()` reads input line and trims whitespace
2. `evaluate()` parses cards, calculates total, optimizes aces
3. `main()` formats and displays result based on bust threshold

## Key Concepts

- **Module System**: Demonstrates import aliasing (`i=io:std.io`, `i=s:std.str`)
- **Mutable Variables**: Uses `mut` keyword for variables that change during execution
- **String Operations**: Extensive use of `std.str` for parsing, conversion, and formatting
- **Control Flow**: Nested conditionals and loops with `lp()` construct
- **Type System**: Explicit type annotations (`$str`, `$i64`) for function signatures
- **Early Returns**: Uses `<value` syntax for early function returns

## Line-by-Line Notes

**Module Imports:**
```toke
m=blackjack;i=io:std.io;i=s:std.str
```
- Declares module name and creates aliases for I/O and string libraries

**Card Value Assignment:**
```toke
if(card="J"){value=10}el{if(card="Q"){value=10}el{if(card="K"){value=10}el{if(card="A"){value=11;aces=aces+1}el{value=s.toint(card)}}}}
```
- Face cards (J,Q,K) = 10 points
- Aces initially = 11 points (tracked separately)
- Numeric cards parsed directly

**Ace Optimization:**
```toke
lp(total>21){if(aces>0){total=total-10;aces=aces-1}el{<total}}
```
- Converts aces from 11 to 1 (subtract 10) while total > 21
- Early return if no more aces available to convert

**Output Logic:**
```toke
if(total>21){io.println(s.concat(s.fromint(total);" Bust"))}el{io.println(s.concat(s.fromint(total);" Safe"))}
```
- Formats output as "[total] Bust" or "[total] Safe"

## Test Coverage

**Recommended test cases should verify:**
- Basic hands without aces: `"5 7"` → `"12 Safe"`
- Face card combinations: `"K Q"` → `"20 Safe"`
- Ace soft/hard totals: `"A 6"` → `"17 Safe"`, `"A A 9"` → `"21 Safe"`
- Bust scenarios: `"K Q 5"` → `"25 Bust"`
- Multiple ace optimization: `"A A A 8"` → `"21 Safe"`
- Edge case: `"A"` → `"11 Safe"`

## Complexity

**Time Complexity:** O(n + a)
- n = number of cards (single pass for parsing and summing)
- a = number of aces (worst case optimization loop)

**Space Complexity:** O(n)
- Stores cards array from string split operation
- Additional O(1) for counters and temporary variables

## Potential Improvements

1. **Error Handling**: Add validation for invalid card inputs and malformed hands
2. **Code Formatting**: Break long conditional chains into more readable structure
3. **Function Decomposition**: Extract card value parsing into separate helper function
4. **Input Validation**: Verify cards are valid blackjack values before processing
5. **Memory Optimization**: Consider streaming card processing to avoid storing entire cards array
6. **Enhanced Output**: Add more detailed game information (soft/hard ace totals)
7. **Performance**: Early termination if bust detected during initial calculation