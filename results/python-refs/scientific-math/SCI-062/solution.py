import sys

# Read input
bins = int(input().strip())
numbers = list(map(float, input().strip().split()))

# Find min and max
min_val = min(numbers)
max_val = max(numbers)

# Calculate bin width
bin_width = (max_val - min_val) / bins

# Create bins and count
bin_counts = [0] * bins
bin_edges = []

for i in range(bins):
    start = min_val + i * bin_width
    end = min_val + (i + 1) * bin_width
    bin_edges.append((start, end))

# Count numbers in each bin
for num in numbers:
    # Find which bin this number belongs to
    bin_index = min(int((num - min_val) / bin_width), bins - 1)
    bin_counts[bin_index] += 1

# Generate output
for i in range(bins):
    start, end = bin_edges[i]
    count = bin_counts[i]
    bar = '#' * count
    
    # Format the range - use integers if they're whole numbers
    if start == int(start):
        start_str = str(int(start))
    else:
        start_str = str(start)
    
    if end == int(end):
        end_str = str(int(end))
    else:
        end_str = str(end)
    
    print(f"[{start_str},{end_str}): {count} {bar}")