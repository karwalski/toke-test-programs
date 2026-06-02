import json
import sys

# Read input
group_def = json.loads(input().strip())
sender = input().strip()
message = input().strip()

# Generate delivery records
delivery_records = []
for member in group_def["members"]:
    if member != sender:
        record = {
            "recipient": member,
            "message": message,
            "group": group_def["name"],
            "sender": sender
        }
        delivery_records.append(record)

# Output JSON array
print(json.dumps(delivery_records, separators=(',', ':')))