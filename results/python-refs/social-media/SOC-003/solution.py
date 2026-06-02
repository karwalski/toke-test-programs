import json
import sys

# Mock user database
users_db = {
    1: {
        "id": 1,
        "username": "alice",
        "bio": "",
        "avatar_url": None,
        "follower_count": 0,
        "following_count": 0
    }
}

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Extract user_id from the request
user_id = input_data["user_id"]

# Fetch user profile
if user_id in users_db:
    profile = users_db[user_id]
    # Output the profile as JSON
    print(json.dumps(profile, separators=(',', ':')))
else:
    # Handle case where user doesn't exist
    print(json.dumps({"error": "User not found"}, separators=(',', ':')))