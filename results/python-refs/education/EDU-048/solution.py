import sys
import math
from collections import Counter

scores = list(map(int, sys.stdin.read().split()))

mean = sum(scores) / len(scores)
sorted_scores = sorted(scores)
n = len(sorted_scores)
if n % 2 == 1:
    median = float(sorted_scores[n // 2])
else:
    median = (sorted_scores[n // 2 - 1] + sorted_scores[n // 2]) / 2

counter = Counter(scores)
max_count = max(counter.values())
modes = [score for score, count in counter.items() if count == max_count]
mode = min(modes)

min_score = min(scores)
max_score = max(scores)

if len(scores) > 1:
    variance = sum((x - mean) ** 2 for x in scores) / (len(scores) - 1)
else:
    variance = 0
stddev = math.sqrt(variance)

passing_scores = sum(1 for score in scores if score >= 50)
pass_rate = (passing_scores / len(scores)) * 100

print(f"mean: {mean:.1f}")
print(f"median: {median:.1f}")
print(f"mode: {mode}")
print(f"min: {min_score}")
print(f"max: {max_score}")
print(f"stddev: {stddev:.1f}")
print(f"pass_rate: {pass_rate:.0f}%")