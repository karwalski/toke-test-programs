import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read())

# Create a dictionary mapping standard IDs to descriptions
standards_map = {}
for standard in input_data["standards"]:
    standards_map[standard["id"]] = standard["description"]

# Process each activity and output the result
for activity in input_data["activities"]:
    activity_name = activity["name"]
    standard_id = activity["standard_id"]
    
    if standard_id in standards_map:
        print(f"{activity_name}: {standards_map[standard_id]}")
    else:
        print(f"{activity_name}: UNALIGNED")