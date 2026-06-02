import json
import sys
from collections import Counter

# Read input from stdin
input_data = sys.stdin.read().strip()

# Parse JSON
records = json.loads(input_data)

# Count reasons
reason_counts = Counter()
for record in records:
    reason_counts[record['reason']] += 1

# Sort by count descending, then by reason alphabetically for ties
sorted_reasons = sorted(reason_counts.items(), key=lambda x: (-x[1], x[0]))

# Output results
for reason, count in sorted_reasons:
    print(f"{reason}: {count} absences")

# Output total
total = sum(reason_counts.values())
print(f"total: {total}")