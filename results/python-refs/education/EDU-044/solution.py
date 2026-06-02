import json
import sys

# Bloom's taxonomy levels
bloom_levels = {
    1: "REMEMBER",
    2: "UNDERSTAND", 
    3: "APPLY",
    4: "ANALYZE",
    5: "EVALUATE",
    6: "CREATE"
}

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Sort activities by level
sorted_activities = sorted(input_data, key=lambda x: x["level"])

# Output sorted activities with level names
for item in sorted_activities:
    level_name = bloom_levels[item["level"]]
    print(f"{level_name}: {item['activity']}")