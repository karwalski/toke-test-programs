import json
import sys

# Read input
config_line = input().strip()
messages_line = input().strip()

# Parse JSON
config = json.loads(config_line)
messages = json.loads(messages_line)

# Extract config values
user = config["user"]
quota_bytes = config["quota_bytes"]
used_bytes = config["used_bytes"]

# Process each message
current_usage = used_bytes

for message in messages:
    msg_id = message["id"]
    size_bytes = message["size_bytes"]
    
    # Check if adding this message would exceed quota
    new_usage = current_usage + size_bytes
    
    if new_usage <= quota_bytes:
        # Accept the message
        current_usage = new_usage
        percentage = int((current_usage / quota_bytes) * 100)
        print(f"{msg_id}: ACCEPTED ({current_usage}/{quota_bytes} = {percentage}%)")
    else:
        # Reject the message
        print(f"{msg_id}: REJECTED (would exceed quota: {new_usage} > {quota_bytes})")

# Final usage report
final_percentage = int((current_usage / quota_bytes) * 100)
print(f"final: {current_usage}/{quota_bytes} bytes ({final_percentage}%)")