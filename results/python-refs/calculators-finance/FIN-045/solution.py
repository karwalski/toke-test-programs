import sys

# Read input
data = list(map(float, input().strip().split(',')))

# Calculate mean
mean = sum(data) / len(data)

# Calculate population variance
pop_variance = sum((x - mean) ** 2 for x in data) / len(data)

# Calculate sample variance
sample_variance = sum((x - mean) ** 2 for x in data) / (len(data) - 1)

# Output results
print(f"{pop_variance:.4f}")
print(f"{sample_variance:.4f}")