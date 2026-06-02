import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract required fields
    action = input_data["action"]
    token = input_data["token"]
    post_id = input_data["post_id"]
    option_id = input_data["option_id"]
    
    # Simple in-memory storage simulation
    # In a real application, this would be a database
    polls = {
        3: {
            "options": [
                {"id": 1, "text": "Red", "votes": 0},
                {"id": 2, "text": "Blue", "votes": 0},
                {"id": 3, "text": "Green", "votes": 0}
            ],
            "voted_users": set()
        }
    }
    
    # Simple token validation (in real app, would decode JWT properly)
    user_id = "user1"  # Extracted from token in real implementation
    
    if action == "vote_poll":
        poll = polls.get(post_id)
        if poll and user_id not in poll["voted_users"]:
            # Add vote
            for option in poll["options"]:
                if option["id"] == option_id:
                    option["votes"] += 1
                    break
            
            # Mark user as voted
            poll["voted_users"].add(user_id)
            
            # Prepare response
            response = {
                "post_id": post_id,
                "voted_option": option_id,
                "results": poll["options"],
                "status": "voted"
            }
        else:
            response = {"error": "Already voted or invalid poll"}
    else:
        response = {"error": "Invalid action"}
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()