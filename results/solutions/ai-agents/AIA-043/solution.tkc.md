# churnrisk.tkc.md

## Overview

This program analyzes customer interaction data in JSON format to assess churn risk and provide engagement recommendations. It parses customer service interactions, evaluates factors like unresolved complaints, cancellation inquiries, and negative sentiment, then outputs a JSON response with risk level and actionable recommendations.

## Architecture

**Module Structure:**
- `churnrisk` - Main module containing analysis logic
- `std.io` - Standard I/O operations for input/output
- `std.str` - String manipulation utilities

**Data Flow:**
1. `main()` reads JSON input via stdin
2. `analyzechurn()` parses interaction data and evaluates risk factors
3. Risk assessment based on complaint resolution, cancellation signals, and sentiment
4. JSON response generation with risk level and recommendations

**Functions:**
- `analyzechurn(data: $str): $str` - Core analysis engine
- `main(): $i64` - Entry point handling I/O

## Key Concepts

**Toke Language Features Demonstrated:**
- **Type System**: Explicit type annotations (`$str`, `$i64`) and mutable variables (`mut`)
- **String Manipulation**: Extensive use of `std.str` for parsing and concatenation
- **Control Flow**: Loop constructs (`lp`) and conditional branching
- **Array Operations**: Dynamic array building with `@()` syntax
- **Module System**: Import aliasing (`i=io:std.io`, `i=s:std.str`)

## Line-by-Line Notes

**Lines 1-3**: Module imports with aliasing for cleaner code
**Lines 4-7**: JSON structure validation using string splitting on interaction markers
**Lines 8-15**: Metric initialization and interaction parsing setup
**Lines 16-25**: Main analysis loop extracting boolean flags from JSON strings
**Lines 26-32**: Risk factor accumulation with complaint and sentiment analysis
**Lines 33-52**: Dynamic factor list building with array manipulation patterns
**Lines 53-60**: Risk-based recommendation assignment
**Lines 61-70**: JSON response construction via string concatenation
**Lines 72-75**: I/O handling in main function

## Test Coverage

**Recommended Test Cases:**
- **Low Risk**: Few interactions, resolved complaints, positive sentiment
- **High Risk - Complaints**: Multiple unresolved complaints
- **High Risk - Cancellation**: Presence of cancellation inquiries
- **High Risk - Sentiment**: Consistently negative feedback across all interactions
- **Edge Cases**: Empty data, malformed JSON, single interaction scenarios
- **Combination Scenarios**: Multiple risk factors present simultaneously

## Complexity

**Time Complexity:** O(n²) where n is the number of interactions
- Primary bottleneck: Array reconstruction operations in factor list building
- String operations are O(m) where m is average interaction length

**Space Complexity:** O(n)
- Stores interaction arrays and factor lists proportional to input size
- String concatenation creates intermediate copies

## Potential Improvements

**Performance Optimizations:**
- Replace array reconstruction with append operations for O(n) factor list building
- Use StringBuilder pattern instead of repeated string concatenation
- Implement proper JSON parser instead of string splitting

**Code Quality:**
- Extract magic strings into named constants
- Separate parsing logic from analysis logic into distinct functions
- Add input validation and error handling for malformed JSON
- Implement structured data types instead of string-based JSON manipulation

**Functionality Enhancements:**
- Support weighted risk scoring instead of binary high/low classification
- Add configurable thresholds for risk factors
- Include timestamp analysis for interaction frequency patterns
- Generate more granular recommendations based on specific factor combinations