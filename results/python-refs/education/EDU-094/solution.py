import json
import sys
from collections import Counter

# Read input from stdin
input_data = sys.stdin.read().strip()
survey_data = json.loads(input_data)

# Count all interests
interest_counter = Counter()
total_students = len(survey_data)

for response in survey_data:
    for interest in response["interests"]:
        interest_counter[interest] += 1

# Sort by count (descending) then by topic name (ascending) for consistent ordering
sorted_interests = sorted(interest_counter.items(), key=lambda x: (-x[1], x[0]))

# Output results
rank = 1
for topic, count in sorted_interests:
    percentage = round((count / total_students) * 100)
    print(f"{rank}. {topic}: {count} votes ({percentage}%)")
    rank += 1