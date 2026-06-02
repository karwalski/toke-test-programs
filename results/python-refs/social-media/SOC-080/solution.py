import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Mock user database
    users_db = {
        1: {"id": 1, "username": "alice"},
        2: {"id": 2, "username": "bob"},
        3: {"id": 3, "username": "carol"},
        4: {"id": 4, "username": "david"}
    }
    
    # Extract data from input
    action = input_data.get("action")
    token = input_data.get("token")
    add_user_ids = input_data.get("add_user_ids", [])
    
    # Build close friends list from the user IDs to add
    close_friends = []
    for user_id in add_user_ids:
        if user_id in users_db:
            close_friends.append(users_db[user_id])
    
    # Create response
    response = {
        "close_friends": close_friends,
        "total": len(close_friends),
        "status": "updated"
    }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()