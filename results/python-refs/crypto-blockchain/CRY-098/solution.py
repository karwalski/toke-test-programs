import json
import sys

# Read input from stdin
input_data = sys.stdin.read().strip()
reports = json.loads(input_data)

# Extract prices
prices = [report['price'] for report in reports]

# Calculate median
prices.sort()
n = len(prices)
if n % 2 == 0:
    median = (prices[n//2 - 1] + prices[n//2]) / 2
else:
    median = prices[n//2]

# Find outliers (>20% from median)
outliers = []
for report in reports:
    price = report['price']
    deviation = abs(price - median) / median
    if deviation > 0.2:
        outliers.append(report['source'])

# Output results
print(int(median) if median == int(median) else median)
if outliers:
    print(','.join(outliers))
else:
    print()