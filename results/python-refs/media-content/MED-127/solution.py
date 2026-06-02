import sys
import re

# Read all input
input_text = sys.stdin.read().strip()

# Split on separator
parts = input_text.split('---')
template = parts[0].strip()
values_block = parts[1].strip()

# Parse key-value pairs
values = {}
for line in values_block.split('\n'):
    if '=' in line:
        key, value = line.split('=', 1)
        values[key] = value

# Find all placeholders in template
placeholders = re.findall(r'\{\{(\w+)\}\}', template)

# Check for missing values
missing = []
for placeholder in placeholders:
    if placeholder not in values:
        missing.append(placeholder)

# Output result
if missing:
    for var in missing:
        print(f"MISSING: {var}")
else:
    print("VALID")