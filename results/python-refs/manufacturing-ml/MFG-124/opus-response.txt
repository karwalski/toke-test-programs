import sys
import csv
import json
from io import StringIO

input_data = sys.stdin.read().strip()
csv_reader = csv.DictReader(StringIO(input_data))
stages = []

for row in csv_reader:
    stages.append({
        'stage': row['stage'],
        'input_qty': int(row['input_qty']),
        'output_qty': int(row['output_qty'])
    })

stage_yields = []
for stage in stages:
    yield_rate = stage['output_qty'] / stage['input_qty']
    stage_yields.append(round(yield_rate, 2))

# Cumulative yield based on overall: first input to last output
if stages:
    cumulative_yield = stages[-1]['output_qty'] / stages[0]['input_qty']
else:
    cumulative_yield = 1.0

min_yield = min(stage_yields)
bottleneck_index = stage_yields.index(min_yield)
bottleneck_stage = stages[bottleneck_index]['stage']

result = {
    "stage_yields": stage_yields,
    "cumulative_yield": round(cumulative_yield, 2),
    "bottleneck_stage": bottleneck_stage
}

print(json.dumps(result, separators=(',', ':')))