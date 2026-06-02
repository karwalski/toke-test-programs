import sys

# Read input
observed_line = input().strip()
expected_line = input().strip()

# Parse frequencies
observed = list(map(float, observed_line.split(',')))
expected = list(map(float, expected_line.split(',')))

# Calculate chi-square statistic
chi_square = 0.0
for i in range(len(observed)):
    chi_square += ((observed[i] - expected[i]) ** 2) / expected[i]

# Output result to 4 decimal places
print(f"{chi_square:.4f}")