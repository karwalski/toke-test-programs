import json
import sys
from itertools import product

# Read JSON input from stdin
input_data = json.load(sys.stdin)

# Get all the axes (keys) and their values
axes = list(input_data.keys())
values = [input_data[axis] for axis in axes]

# Generate all combinations using cartesian product
combinations = list(product(*values))

# Output each combination in YAML format
for combination in combinations:
    print("-", end="")
    for i, axis in enumerate(axes):
        print(f" {axis}: {combination[i]}")