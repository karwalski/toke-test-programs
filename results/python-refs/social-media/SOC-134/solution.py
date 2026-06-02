import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract required fields
    action = input_data.get("action")
    token = input_data.get("token")
    post_id = input_data.get("post_id")
    conversation_id = input_data.get("conversation_id")
    message = input_data.get("message")
    
    # Create response based on the expected output format
    response = {
        "message_id": "msg_3",
        "type": "shared_post",
        "post_id": post_id,
        "message": message,
        "status": "sent"
    }
    
    # Output JSON response to stdout
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()