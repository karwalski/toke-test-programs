import json
import sys
from collections import Counter

# Read input from stdin
input_data = sys.stdin.read().strip()

# Parse JSON input
records = json.loads(input_data)

# Count error topics across all students and tests
error_counts = Counter()

for record in records:
    wrong_topics = record.get("wrong_topics", [])
    for topic in wrong_topics:
        error_counts[topic] += 1

# Sort by frequency (descending), then by topic name (ascending) for ties
sorted_errors = sorted(error_counts.items(), key=lambda x: (-x[1], x[0]))

# Output results in the required format
for topic, count in sorted_errors:
    print(f"{topic}: {count} errors")