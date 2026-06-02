import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Mock data for DM conversations sorted by last activity
    conversations = [
        {
            "id": "conv_1",
            "participants": ["alice", "bob"],
            "last_message": "Hey!",
            "last_at": "2026-01-01T00:00:00Z",
            "unread": 0
        }
    ]
    
    # Create response
    response = {
        "conversations": conversations,
        "next_cursor": None
    }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()