import sys
from collections import Counter

# Read all input lines
lines = []
for line in sys.stdin:
    lines.append(line.strip())

# Count frequencies
counter = Counter(lines)

# Sort by count descending, then by value ascending
sorted_items = sorted(counter.items(), key=lambda x: (-x[1], x[0]))

# Output results
for value, count in sorted_items:
    print(f"{value}\t{count}")