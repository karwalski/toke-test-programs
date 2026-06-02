import sys
import json
import re

# Read all input
input_data = sys.stdin.read()

# Split on the separator
parts = input_data.split('---')
template = parts[0]
json_vars = parts[1].strip()

# Parse the JSON variables
variables = json.loads(json_vars)

# Replace placeholders in template
def replace_var(match):
    var_name = match.group(1)
    return str(variables[var_name])

# Use regex to find and replace {{var}} patterns
result = re.sub(r'\{\{(\w+)\}\}', replace_var, template)

# Output the result
sys.stdout.write(result)