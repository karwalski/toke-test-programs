import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Extract the decision and requester_id
decision = input_data["decision"]
requester_id = input_data["requester_id"]

# Create response based on decision
if decision == "accept":
    response = {
        "requester_id": requester_id,
        "decision": "accepted", 
        "status": "now_following"
    }
elif decision == "reject":
    response = {
        "requester_id": requester_id,
        "decision": "rejected",
        "status": "request_declined"
    }

# Output JSON response
print(json.dumps(response, separators=(',', ':')))