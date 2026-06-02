import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

plan = input_data['plan']
pricing = input_data['pricing']

# Initialize breakdown dictionary
breakdown = {}
total_cost = 0

# Process each tool call in the plan
for tool_call in plan:
    tool_name = tool_call['tool']
    
    # Initialize tool in breakdown if not seen before
    if tool_name not in breakdown:
        breakdown[tool_name] = {"count": 0, "cost": 0}
    
    # Increment count and add to cost
    breakdown[tool_name]["count"] += 1
    tool_cost = pricing[tool_name]
    breakdown[tool_name]["cost"] += tool_cost
    total_cost += tool_cost

# Create output
output = {
    "total_cost": total_cost,
    "breakdown": breakdown
}

# Print JSON output
print(json.dumps(output, separators=(',', ':')))