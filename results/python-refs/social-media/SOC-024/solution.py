import json
import sys

# Simple in-memory storage for demo purposes
pinned_posts = []

def pin_post(post_id):
    # Remove post if already pinned
    pinned_posts[:] = [p for p in pinned_posts if p != post_id]
    
    # Add to beginning of list
    pinned_posts.insert(0, post_id)
    
    # Keep only max 3 pinned posts
    if len(pinned_posts) > 3:
        pinned_posts[:] = pinned_posts[:3]
    
    # Get position (1-indexed)
    pin_position = pinned_posts.index(post_id) + 1
    
    return {
        "post_id": post_id,
        "pinned": True,
        "pin_position": pin_position,
        "status": "pinned"
    }

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Process the request
if input_data.get("action") == "pin_post":
    post_id = input_data.get("post_id")
    response = pin_post(post_id)
    print(json.dumps(response, separators=(',', ':')))