import sys

# Read input
lines = sys.stdin.read().strip().split('\n')
bin_count = int(lines[0])
values = list(map(float, lines[1].split()))

# Find min and max values
min_val = min(values)
max_val = max(values)

# Calculate bin width
bin_width = (max_val - min_val) / bin_count

# Create bins and count values
bins = [0] * bin_count

for value in values:
    # Determine which bin this value belongs to
    bin_index = int((value - min_val) / bin_width)
    # Handle edge case where value equals max_val
    if bin_index == bin_count:
        bin_index = bin_count - 1
    bins[bin_index] += 1

# Generate output
for i in range(bin_count):
    bin_start = min_val + i * bin_width
    bin_end = min_val + (i + 1) * bin_width
    count = bins[i]
    
    # Format the histogram line
    bar = "#" * count
    print(f"{bin_start:4.1f}-{bin_end:4.1f}: {bar} ({count})")