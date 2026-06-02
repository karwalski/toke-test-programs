import json
import sys
import hashlib
import hmac
import base64

# Simulated database
posts = {
    1: {"id": 1, "author_id": 1, "content": "Test post", "deleted": False},
    2: {"id": 2, "author_id": 2, "content": "Another post", "deleted": False}
}

users = {
    1: {"id": 1, "username": "user1", "role": "user"},
    2: {"id": 2, "username": "user2", "role": "user"},
    3: {"id": 3, "username": "mod1", "role": "moderator"}
}

# Simple token validation (simulated)
def validate_token(token):
    # For this simulation, we'll decode a simple token format
    # In real implementation, this would use proper JWT validation
    try:
        # Assuming token format: base64(user_id)
        decoded = base64.b64decode(token + "==").decode('utf-8')
        user_id = int(decoded)
        return users.get(user_id)
    except:
        return None

def can_delete_post(user, post):
    if not user or not post:
        return False
    
    # Author can delete their own post
    if post["author_id"] == user["id"]:
        return True
    
    # Moderator can delete any post
    if user["role"] == "moderator":
        return True
    
    return False

def delete_post(token, post_id):
    # Validate token and get user
    user = validate_token(token)
    if not user:
        return {"error": "Invalid token"}
    
    # Get post
    post = posts.get(post_id)
    if not post:
        return {"error": "Post not found"}
    
    if post["deleted"]:
        return {"error": "Post already deleted"}
    
    # Check permissions
    if not can_delete_post(user, post):
        return {"error": "Permission denied"}
    
    # Soft delete the post
    post["deleted"] = True
    
    return {"post_id": post_id, "status": "deleted"}

# Read input from stdin
input_data = sys.stdin.read().strip()
request = json.loads(input_data)

# Process request
if request.get("action") == "delete_post":
    result = delete_post(request.get("token"), request.get("post_id"))
    print(json.dumps(result, separators=(',', ':')))
else:
    print(json.dumps({"error": "Invalid action"}, separators=(',', ':')))