import json
import sys

def get_reactions(post_id):
    # Mock data - in a real application, this would come from a database
    mock_data = {
        1: {
            "reactions": {"heart": 5, "laugh": 3, "fire": 2},
            "total": 10,
            "top_reactors": [{"username": "bob", "emoji": "heart"}]
        }
    }
    
    if post_id in mock_data:
        return {
            "post_id": post_id,
            "reactions": mock_data[post_id]["reactions"],
            "total": mock_data[post_id]["total"],
            "top_reactors": mock_data[post_id]["top_reactors"]
        }
    else:
        return {
            "post_id": post_id,
            "reactions": {},
            "total": 0,
            "top_reactors": []
        }

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Process the request
if input_data["action"] == "get_reactions":
    post_id = input_data["post_id"]
    result = get_reactions(post_id)
    
    # Output JSON response
    print(json.dumps(result, separators=(',', ':')))