import sys

# Read monthly budget
budget = float(input().strip())

# Read expense entries and calculate total spent
total_spent = 0.0

for line in sys.stdin:
    line = line.strip()
    if line:
        parts = line.split()
        amount = float(parts[2])
        total_spent += amount

# Calculate remaining budget
remaining = budget - total_spent

# Determine status
status = "UNDER" if remaining >= 0 else "OVER"

# Output results
print(f"{total_spent:.2f}")
print(f"{remaining:.2f}")
print(status)