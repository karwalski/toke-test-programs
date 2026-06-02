import sys
import statistics
import math
from collections import Counter

# Read input from stdin
scores = list(map(int, input().split()))

# Calculate statistics
mean = sum(scores) / len(scores)
median = statistics.median(scores)

# Find mode (most frequent value)
counter = Counter(scores)
max_count = max(counter.values())
modes = [score for score, count in counter.items() if count == max_count]
mode = min(modes)  # If multiple modes, take the smallest

# Min and max
min_score = min(scores)
max_score = max(scores)

# Standard deviation (sample standard deviation)
variance = sum((x - mean) ** 2 for x in scores) / (len(scores) - 1)
stddev = math.sqrt(variance)

# Pass rate (>= 50)
passing_scores = sum(1 for score in scores if score >= 50)
pass_rate = (passing_scores / len(scores)) * 100

# Output with exact formatting
print(f"mean: {mean:.1f}")
print(f"median: {median:.1f}")
print(f"mode: {mode}")
print(f"min: {min_score}")
print(f"max: {max_score}")
print(f"stddev: {stddev:.1f}")
print(f"pass_rate: {pass_rate:.0f}%")