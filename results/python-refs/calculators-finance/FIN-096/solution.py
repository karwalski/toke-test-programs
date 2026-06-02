import sys
from math import gcd
from functools import reduce

# Read input from stdin
input_line = sys.stdin.read().strip()

# Parse comma-separated integers
numbers = [int(x.strip()) for x in input_line.split(',')]

# Calculate GCD of all numbers using reduce
result = reduce(gcd, numbers)

# Output the result
print(result)