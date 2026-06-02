import json
import sys

# Mock data for users and their followers
users_db = {
    1: {"id": 1, "username": "alice", "followers": [3, 4, 5]},
    2: {"id": 2, "username": "bob", "followers": [3, 6, 7]},
    3: {"id": 3, "username": "carol", "followers": [1, 2]},
    4: {"id": 4, "username": "dave", "followers": []},
    5: {"id": 5, "username": "eve", "followers": []},
    6: {"id": 6, "username": "frank", "followers": []},
    7: {"id": 7, "username": "grace", "followers": []}
}

def find_mutual_followers(user_id_a, user_id_b, limit):
    # Get followers for both users
    followers_a = set(users_db.get(user_id_a, {}).get("followers", []))
    followers_b = set(users_db.get(user_id_b, {}).get("followers", []))
    
    # Find mutual followers
    mutual_follower_ids = followers_a.intersection(followers_b)
    
    # Convert to list and sort for consistent output
    mutual_follower_ids = sorted(list(mutual_follower_ids))
    
    # Apply limit
    mutual_follower_ids = mutual_follower_ids[:limit]
    
    # Build response with user details
    mutual_followers = []
    for user_id in mutual_follower_ids:
        if user_id in users_db:
            mutual_followers.append({
                "id": user_id,
                "username": users_db[user_id]["username"]
            })
    
    return {
        "mutual": mutual_followers,
        "total": len(mutual_followers)
    }

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Extract parameters
action = input_data["action"]
user_id_a = input_data["user_id_a"]
user_id_b = input_data["user_id_b"]
limit = input_data["limit"]

# Process request
if action == "mutual_followers":
    result = find_mutual_followers(user_id_a, user_id_b, limit)
    print(json.dumps(result, separators=(',', ':')))