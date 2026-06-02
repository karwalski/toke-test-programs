import json
import sys

# Read input
tier_limits = json.loads(input().strip())
conversation = json.loads(input().strip())
add_requests = json.loads(input().strip())

# Extract conversation details
conv_type = conversation["type"]
current_members = conversation["current_members"]
tier = conversation["tier"]

# Get the limit for this conversation type and tier
limit = tier_limits[tier][conv_type]

# Process each add request
members_count = current_members
for username in add_requests:
    if members_count < limit:
        members_count += 1
        print(f"{username}: ALLOWED ({members_count}/{limit})")
    else:
        print(f"{username}: REJECTED (would exceed limit: {limit} for {tier}/{conv_type})")

print(f"final members: {members_count}")