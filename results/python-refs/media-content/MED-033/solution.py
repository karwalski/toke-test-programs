import sys

# Read all input
content = sys.stdin.read()

# Split on '---' separator
parts = content.split('---')
template = parts[0]
variables_block = parts[1]

# Parse variables
variables = {}
for line in variables_block.strip().split('\n'):
    if '=' in line:
        key, value = line.split('=', 1)
        variables[key] = value

# Replace placeholders
result = template
for key, value in variables.items():
    placeholder = '{{' + key + '}}'
    result = result.replace(placeholder, value)

# Output the result
print(result, end='')