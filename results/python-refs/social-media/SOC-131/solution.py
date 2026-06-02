import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Mock user database
    users = {
        1: {"id": 1, "username": "alice"},
        2: {"id": 2, "username": "bob"},
        3: {"id": 3, "username": "carol"},
        4: {"id": 4, "username": "dave"}
    }
    
    # Extract data from input
    action = input_data.get("action")
    token = input_data.get("token")
    participant_ids = input_data.get("participant_ids", [])
    name = input_data.get("name")
    
    # Assume token represents user ID 1 (alice)
    current_user_id = 1
    
    # Build participants list including current user
    all_participant_ids = [current_user_id] + participant_ids
    participants = []
    
    for user_id in all_participant_ids:
        if user_id in users:
            participants.append(users[user_id])
    
    # Create response
    response = {
        "conversation_id": "conv_2",
        "name": name,
        "participants": participants,
        "status": "created"
    }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()