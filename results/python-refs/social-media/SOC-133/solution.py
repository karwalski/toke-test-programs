import json
import sys

def get_read_receipts(request):
    # Mock data for read receipts
    mock_receipts = {
        "msg_1": [{"user": "bob", "read_at": "2026-01-01T00:01:00Z"}],
        "msg_2": []
    }
    
    message_ids = request.get("message_ids", [])
    receipts = []
    
    for message_id in message_ids:
        read_by = mock_receipts.get(message_id, [])
        receipts.append({
            "message_id": message_id,
            "read_by": read_by
        })
    
    return {"receipts": receipts}

# Read input from stdin
input_data = sys.stdin.read().strip()
request = json.loads(input_data)

# Process the request
response = get_read_receipts(request)

# Output response to stdout
print(json.dumps(response, separators=(',', ':')))