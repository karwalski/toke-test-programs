# Read values and weights from stdin
values_line = input().strip()
weights_line = input().strip()

# Parse values and weights
values = [float(x) for x in values_line.split(',')]
weights = [float(x) for x in weights_line.split(',')]

# Calculate weighted average
weighted_sum = sum(v * w for v, w in zip(values, weights))
weight_sum = sum(weights)
weighted_average = weighted_sum / weight_sum

# Output to 4 decimal places
print(f"{weighted_average:.4f}")