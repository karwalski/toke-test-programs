import sys

# Read input
percentile = float(input().strip())
numbers = list(map(float, input().strip().split(',')))

# Sort the numbers
numbers.sort()

# Calculate percentile using linear interpolation
n = len(numbers)
index = (percentile / 100) * (n - 1)

# Get the lower and upper indices
lower_index = int(index)
upper_index = lower_index + 1

# Handle edge cases
if upper_index >= n:
    result = numbers[-1]
else:
    # Linear interpolation
    lower_value = numbers[lower_index]
    upper_value = numbers[upper_index]
    fraction = index - lower_index
    result = lower_value + fraction * (upper_value - lower_value)

# Output with 4 decimal places
print(f"{result:.4f}")