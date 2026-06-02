import sys
import math
from collections import Counter

line = sys.stdin.read().strip()
numbers = list(map(float, line.split()))
n = len(numbers)

mean = sum(numbers) / n

sorted_nums = sorted(numbers)
if n % 2 == 0:
    median = (sorted_nums[n//2 - 1] + sorted_nums[n//2]) / 2
else:
    median = sorted_nums[n//2]

counter = Counter(numbers)
max_count = max(counter.values())
modes = [k for k, v in counter.items() if v == max_count]

if len(modes) == 1:
    mode_str = str(int(modes[0]) if modes[0].is_integer() else modes[0])
else:
    mode_str = "MULTIMODAL"

# Population variance
variance = sum((x - mean) ** 2 for x in numbers) / n
std_dev = math.sqrt(variance)

if n >= 3 and std_dev > 0:
    skewness = sum((x - mean) ** 3 for x in numbers) / n / (std_dev ** 3)
else:
    skewness = 0.0

if n >= 3 and std_dev > 0:
    kurtosis = sum((x - mean) ** 4 for x in numbers) / n / (std_dev ** 4) - 3
else:
    kurtosis = 0.0

print(f"Mean: {mean:.4f}")
print(f"Median: {median:.4f}")
print(f"Mode: {mode_str}")
print(f"Variance: {variance:.4f}")
print(f"StdDev: {std_dev:.4f}")
print(f"Skewness: {skewness:.4f}")
print(f"Kurtosis: {kurtosis:.4f}")