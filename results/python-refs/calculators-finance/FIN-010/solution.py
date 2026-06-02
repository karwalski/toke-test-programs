import sys

variables = {}
lines = []

# Read all input
for line in sys.stdin:
    lines.append(line.strip())

# Process each line
for line in lines[:-1]:  # All lines except the last one are variable assignments
    if '=' in line:
        var_name, value = line.split(' = ')
        variables[var_name] = int(value)

# The last line is the expression to evaluate
expression = lines[-1]

# Replace variables in the expression with their values
for var_name, value in variables.items():
    expression = expression.replace(var_name, str(value))

# Evaluate and print the result
result = eval(expression)
print(result)