import re
import sys

# Read input from stdin
text = sys.stdin.read().strip()

# Find all template variables in both {{var}} and ${var} formats
pattern = r'\{\{([^}]+)\}\}|\$\{([^}]+)\}'
matches = re.findall(pattern, text)

# Extract variable names (matches returns tuples, we need non-empty groups)
variables = set()
for match in matches:
    var_name = match[0] if match[0] else match[1]
    variables.add(var_name.strip())

# Sort alphabetically and print one per line
for var in sorted(variables):
    print(var)