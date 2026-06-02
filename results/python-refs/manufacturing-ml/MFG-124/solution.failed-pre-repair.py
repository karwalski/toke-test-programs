import sys
import csv
import json
from io import StringIO

# Read input from stdin
input_data = sys.stdin.read().strip()

# Parse CSV data
csv_reader = csv.DictReader(StringIO(input_data))
stages = []

for row in csv_reader:
    stages.append({
        'stage': row['stage'],
        'input_qty': int(row['input_qty']),
        'output_qty': int(row['output_qty'])
    })

# Calculate stage yields
stage_yields = []
for stage in stages:
    yield_rate = stage['output_qty'] / stage['input_qty']
    stage_yields.append(round(yield_rate, 2))

# Calculate cumulative yield
cumulative_yield = 1.0
for yield_rate in stage_yields:
    cumulative_yield *= yield_rate

# Find bottleneck stage (lowest yield)
min_yield = min(stage_yields)
bottleneck_index = stage_yields.index(min_yield)
bottleneck_stage = stages[bottleneck_index]['stage']

# Create output
result = {
    "stage_yields": stage_yields,
    "cumulative_yield": round(cumulative_yield, 2),
    "bottleneck_stage": bottleneck_stage
}

# Output JSON
print(json.dumps(result, separators=(',', ':')))