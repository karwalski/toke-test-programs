import json
import sys
from datetime import datetime

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract required fields
    action = input_data.get("action")
    token = input_data.get("token")
    recipient_id = input_data.get("recipient_id")
    content = input_data.get("content")
    
    # Validate action
    if action != "send_dm":
        return
    
    # Create response with expected format
    response = {
        "message_id": "msg_1",
        "conversation_id": "conv_1", 
        "content": content,
        "sent_at": "2026-01-01T00:00:00Z",
        "status": "sent"
    }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()