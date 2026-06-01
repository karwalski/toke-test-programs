# Pressure Unit Converter - Toke Program Documentation (.tkc.md)

## Overview

This Toke program implements a command-line pressure unit converter that reads user input and converts between different pressure units including Pascals (Pa), kilopascals (kPa), bar, atmospheres (atm), pounds per square inch (psi), and millimeters of mercury (mmHg). The program uses a two-stage conversion process: first normalizing all inputs to Pascals, then converting from Pascals to the target unit.

## Architecture

The program consists of two main functions within a single module:

- **Module `conv`**: Main program module containing conversion logic
- **Function `convert()`**: Core conversion engine that handles unit-to-unit transformations
- **Function `main()`**: Entry point that handles I/O, input parsing, and orchestrates the conversion
- **Data Flow**: Input → Parsing → Conversion → Formatted Output

The architecture follows a simple pipeline pattern where raw input flows through parsing, computation, and formatting stages.

## Key Concepts

- **Type System**: Demonstrates explicit type annotations (`$f64`, `$i64`, `$str`)
- **Mutable Variables**: Uses `mut` keyword for variables that change during execution
- **Module System**: Imports from standard library (`std.io`, `std.str`)
- **String Processing**: Utilizes string splitting, parsing, and formatting operations
- **Conditional Logic**: Nested if-else chains for unit recognition
- **Function Parameters**: Pass-by-value semantics with typed parameters

## Line-by-Line Notes

**Imports & Setup:**
- `m=conv`: Defines module name
- `i=io:std.io`: Aliases standard I/O library
- `i=s:std.str`: Aliases string manipulation library (note: reuses `i` variable)

**Convert Function Logic:**
- Lines with `fromval=val*[factor]`: Convert input unit to Pascals using conversion factors
- Conversion factors: kPa(1000), bar(100000), atm(101325), psi(6894.76), mmHg(133.322)
- Lines with `result=fromval/[factor]`: Convert from Pascals to target unit
- Default case falls through to return Pascals if unit not recognized

**Main Function Flow:**
- `io.readln()`: Read input line from user
- `s.split(line;" ")`: Parse input into space-separated components
- Input validation checks for minimum 3 parts (value, from-unit, to-unit)
- `s.tofloat()`: Parse numeric value from string
- `s.format(result;"%.4f")`: Format output to 4 decimal places

## Test Coverage

To properly test this program, verify:

1. **Basic Conversions**: Each unit pair combination (6×6 = 36 test cases)
2. **Edge Cases**: Zero values, very large/small numbers
3. **Input Validation**: Malformed input, insufficient parameters
4. **Unknown Units**: Behavior with unrecognized unit strings
5. **Precision**: Accuracy of floating-point calculations
6. **Round-trip**: Converting A→B→A should return original value

Example test inputs:
```
1013.25 hPa kPa  # Should output 1.0133
14.7 psi atm     # Should output 1.0007
760 mmHg Pa      # Should output 101325.0000
```

## Complexity

**Time Complexity**: O(1) - Fixed number of string comparisons regardless of input size
**Space Complexity**: O(1) - Uses fixed amount of memory for variables

The nested if-else chains create a maximum of 5 comparisons per conversion stage, making the algorithm constant time with respect to input size.

## Potential Improvements

1. **Unit Recognition**: Replace nested if-else with hash map/dictionary lookup for O(1) unit recognition
2. **Error Handling**: Add validation for invalid units and malformed numeric inputs
3. **Code Organization**: Extract conversion factors into constants or configuration
4. **Input Format**: Support more flexible input formats (e.g., "100 Pa to kPa")
5. **Additional Units**: Add support for torr, inHg, and other pressure units
6. **Precision**: Consider using higher precision arithmetic for scientific applications
7. **Interactive Mode**: Allow multiple conversions without restarting the program
8. **Help System**: Add usage instructions and list of supported units

**Refactoring Suggestion**: The conversion logic could be simplified using a factor table:
```toke
factors = {"Pa": 1.0, "kPa": 1000.0, "bar": 100000.0, ...}
result = val * factors[from] / factors[to]
```