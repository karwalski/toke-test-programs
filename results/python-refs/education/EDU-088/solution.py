import sys

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

# Parse input
classroom_name = lines[0]
rules = lines[1:]

# Format output
border = "=" * 24
title = f"   RULES FOR {classroom_name}   "

print(border)
print(title)
print(border)

for i, rule in enumerate(rules, 1):
    print(f"{i}. {rule}")

print(border)