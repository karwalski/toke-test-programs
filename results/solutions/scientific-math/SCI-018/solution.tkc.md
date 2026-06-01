# Bellman-Ford Algorithm Documentation (.tkc.md)

## Overview

This program implements the Bellman-Ford algorithm to find shortest paths from a single source vertex to all other vertices in a weighted directed graph. It can detect negative cycles and reports either the shortest distances or the presence of a negative cycle that makes shortest paths undefined.

## Architecture

The program follows a monolithic structure within a single `main()` function:

1. **Input Parsing Phase**: Reads graph specification (vertices, edges, weights) and source vertex
2. **Initialization Phase**: Sets up distance array with infinity values, except source (distance 0)
3. **Relaxation Phase**: Performs (n-1) iterations of edge relaxation to find shortest paths
4. **Negative Cycle Detection**: Additional iteration to detect if negative cycles exist
5. **Output Phase**: Prints either "NEGATIVE CYCLE" or shortest distances for each vertex

**Data Flow**: Input → Edge List → Distance Array → Iterative Updates → Cycle Check → Output

## Key Concepts

- **Module System**: Imports `std.io` and `std.str` with aliases (`io`, `s`)
- **Mutable Variables**: Extensive use of `mut.` for counters, arrays, and state tracking
- **Array Operations**: Dynamic array building with `+@()` concatenation
- **Nested Arrays**: Edges stored as arrays of 3-element arrays `@(u,v,w)`
- **Control Flow**: `lp()` loops for iteration, `if/el` conditionals
- **String Manipulation**: Parsing integers from split strings, formatting output
- **Infinity Representation**: Uses `999999` as pseudo-infinity value

## Line-by-Line Notes

**Lines 1-8**: Input parsing - reads n vertices, m edges, then m lines of edge data (u,v,weight)

**Lines 9-15**: Distance array initialization - creates array of size n, all values set to infinity except source vertex (set to 0)

**Lines 16-26**: Core Bellman-Ford relaxation - runs (n-1) iterations, checking each edge for potential distance improvements. When improvement found, rebuilds entire distance array.

**Lines 27-33**: Negative cycle detection - performs one additional relaxation iteration; if any distance can still be improved, a negative cycle exists

**Lines 34-40**: Output formatting - prints "NEGATIVE CYCLE" or formats distances as "vertex: distance" (showing "INF" for unreachable vertices)

## Test Coverage

Expected test scenarios:
- **Basic shortest path**: Simple connected graph without negative cycles
- **Disconnected vertices**: Some vertices unreachable from source
- **Negative weights**: Graph with negative edges but no negative cycles  
- **Negative cycle detection**: Graph containing negative cycles
- **Single vertex**: Edge case with n=1
- **No edges**: Graph with vertices but no connections

## Complexity

- **Time Complexity**: O(V×E) where V is vertices and E is edges
  - (n-1) iterations × m edge relaxations = O(n×m)
  - Additional O(n×m) for negative cycle detection
- **Space Complexity**: O(V + E) 
  - O(n) for distance array
  - O(m) for edge storage
  - Note: Inefficient due to array rebuilding instead of in-place updates

## Potential Improvements

1. **Performance**: Replace array rebuilding with in-place distance updates using mutable array indexing
2. **Memory**: Use single distance array instead of creating new arrays each iteration  
3. **Code Organization**: Extract input parsing, algorithm core, and output into separate functions
4. **Constants**: Define proper infinity constant instead of magic number `999999`
5. **Error Handling**: Add validation for input format and bounds checking
6. **Readability**: Add whitespace, meaningful variable names, and break into logical sections
7. **Early Termination**: Stop relaxation early if no improvements made in an iteration
8. **Output Format**: More structured output format for distances and better negative cycle reporting