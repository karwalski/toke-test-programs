import math

# Read input
data = list(map(float, input().split(',')))

# Calculate mean
n = len(data)
mean = sum(data) / n

# Calculate variance for population and sample
variance_pop = sum((x - mean) ** 2 for x in data) / n
variance_sample = sum((x - mean) ** 2 for x in data) / (n - 1)

# Calculate standard deviations
pop_stdev = math.sqrt(variance_pop)
sample_stdev = math.sqrt(variance_sample)

# Output with 4 decimal places
print(f"{pop_stdev:.4f}")
print(f"{sample_stdev:.4f}")