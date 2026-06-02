import sys
import csv
import json
import math

# Read CSV from stdin
reader = csv.DictReader(sys.stdin)
counts = []

for row in reader:
    counts.append(int(row['count']))

# Calculate total
total = sum(counts)

# Calculate Shannon entropy
entropy = 0.0
for count in counts:
    if count > 0:
        p = count / total
        entropy -= p * math.log2(p)

# Calculate maximum entropy (uniform distribution)
n = len(counts)
max_entropy = math.log2(n) if n > 0 else 0.0

# Calculate normalized entropy
normalised_entropy = entropy / max_entropy if max_entropy > 0 else 0.0

# Output JSON
result = {
    "entropy": entropy,
    "max_entropy": max_entropy,
    "normalised_entropy": normalised_entropy
}

print(json.dumps(result, separators=(',', ':')))