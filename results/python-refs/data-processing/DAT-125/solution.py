import sys

# Read input data
data = []
for line in sys.stdin:
    line = line.strip()
    if line:
        parts = line.split()
        category = parts[0]
        value = int(parts[1])
        data.append((category, value))

# Sort by value in descending order
data.sort(key=lambda x: x[1], reverse=True)

# Calculate total
total = sum(value for _, value in data)

# Calculate cumulative percentages and find 80% threshold
cumulative = 0
threshold_crossed = False
results = []

for category, value in data:
    cumulative += value
    cum_percent = (cumulative / total) * 100
    
    # Check if this is where we cross 80% threshold
    prev_cumulative = cumulative - value
    prev_percent = (prev_cumulative / total) * 100
    
    if prev_percent < 80 and cum_percent >= 80 and not threshold_crossed:
        threshold_crossed = True
        results.append((category, value, cum_percent, True))
    elif prev_percent < 80 and not threshold_crossed:
        results.append((category, value, cum_percent, False))
    else:
        results.append((category, value, cum_percent, None))

# Print header
print("Category  Value  Cum%")

# Print results
for category, value, cum_percent, threshold_status in results:
    if threshold_status is False:
        print(f"{category}           {value}  {cum_percent:.1f}% ← 80% threshold not yet reached")
    elif threshold_status is True:
        print(f"{category}           {value}  {cum_percent:.1f}% ← 80% threshold crossed")
    else:
        print(f"{category}           {value} {cum_percent:.1f}%")