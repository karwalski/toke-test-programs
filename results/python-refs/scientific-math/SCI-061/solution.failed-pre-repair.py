import sys
import math
from collections import Counter

def calculate_skewness(data, mean, std_dev, n):
    if std_dev == 0:
        return 0.0
    skew_sum = sum((x - mean) ** 3 for x in data)
    return (n * skew_sum) / ((n - 1) * (n - 2) * std_dev ** 3)

def calculate_kurtosis(data, mean, std_dev, n):
    if std_dev == 0:
        return 0.0
    kurt_sum = sum((x - mean) ** 4 for x in data)
    return (n * (n + 1) * kurt_sum) / ((n - 1) * (n - 2) * (n - 3) * std_dev ** 4) - (3 * (n - 1) ** 2) / ((n - 2) * (n - 3))

# Read input
line = input().strip()
numbers = list(map(float, line.split()))
n = len(numbers)

# Mean
mean = sum(numbers) / n

# Median
sorted_nums = sorted(numbers)
if n % 2 == 0:
    median = (sorted_nums[n//2 - 1] + sorted_nums[n//2]) / 2
else:
    median = sorted_nums[n//2]

# Mode
counter = Counter(numbers)
max_count = max(counter.values())
modes = [k for k, v in counter.items() if v == max_count]

if len(modes) == 1:
    mode_str = str(int(modes[0]) if modes[0].is_integer() else modes[0])
else:
    mode_str = "MULTIMODAL"

# Variance (sample variance)
variance = sum((x - mean) ** 2 for x in numbers) / (n - 1)

# Standard deviation
std_dev = math.sqrt(variance)

# Skewness and Kurtosis
if n >= 3:
    skewness = calculate_skewness(numbers, mean, std_dev, n)
else:
    skewness = 0.0

if n >= 4:
    kurtosis = calculate_kurtosis(numbers, mean, std_dev, n)
else:
    kurtosis = 0.0

# Output
print(f"Mean: {mean:.4f}")
print(f"Median: {median:.4f}")
print(f"Mode: {mode_str}")
print(f"Variance: {variance:.4f}")
print(f"StdDev: {std_dev:.4f}")
print(f"Skewness: {skewness:.4f}")
print(f"Kurtosis: {kurtosis:.4f}")