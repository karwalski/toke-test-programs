import json
import sys

# Read input from stdin
input_data = json.load(sys.stdin)

stages = input_data['stages']
total_budget_ms = input_data['total_budget_ms']

# Calculate total actual time
total_actual_ms = sum(stage['actual_ms'] for stage in stages)

# Calculate budget remaining
budget_remaining_ms = total_budget_ms - total_actual_ms

# Determine if over budget
over_budget = total_actual_ms > total_budget_ms

# Find slow stages (stages that exceed their individual budget)
slow_stages = []
for stage in stages:
    if stage['actual_ms'] > stage['budget_ms']:
        over_by_ms = stage['actual_ms'] - stage['budget_ms']
        slow_stages.append({
            'name': stage['name'],
            'over_by_ms': over_by_ms
        })

# Create output
output = {
    'total_actual_ms': total_actual_ms,
    'budget_remaining_ms': budget_remaining_ms,
    'over_budget': over_budget,
    'slow_stages': slow_stages
}

# Write output to stdout
print(json.dumps(output, separators=(',', ':')))