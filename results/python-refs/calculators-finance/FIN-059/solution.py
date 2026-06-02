import sys

# Dictionary to store category totals
categories = {}

# Read input from stdin
for line in sys.stdin:
    line = line.strip()
    if line:
        parts = line.split()
        category = parts[0]
        amount = float(parts[1])
        
        if category in categories:
            categories[category] += amount
        else:
            categories[category] = amount

# Calculate total amount
total_amount = sum(categories.values())

# Create list of (category, amount, percentage) tuples
results = []
for category, amount in categories.items():
    percentage = (amount / total_amount) * 100
    results.append((category, amount, percentage))

# Sort by amount descending
results.sort(key=lambda x: x[1], reverse=True)

# Print results
for category, amount, percentage in results:
    print(f"{category} {amount:.2f} {percentage:.2f}%")