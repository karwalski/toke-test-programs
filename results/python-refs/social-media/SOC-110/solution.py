import json
import sys

def validate_token(token):
    # Simple token validation - in real implementation this would verify JWT
    return token.startswith("eyJ")

def bulk_remove_posts(user_id, post_ids):
    # Simulate post removal - in real implementation this would interact with database
    removed = []
    failed = []
    
    for post_id in post_ids:
        # For this simulation, assume all posts exist and can be removed
        removed.append(post_id)
    
    return removed, failed

def main():
    # Read JSON input from stdin
    input_data = json.loads(sys.stdin.read())
    
    action = input_data.get("action")
    token = input_data.get("token")
    user_id = input_data.get("user_id")
    post_ids = input_data.get("post_ids", [])
    
    # Validate action
    if action != "bulk_remove":
        response = {"error": "Invalid action", "status": "failed"}
    elif not validate_token(token):
        response = {"error": "Invalid token", "status": "failed"}
    else:
        # Perform bulk removal
        removed, failed = bulk_remove_posts(user_id, post_ids)
        
        response = {
            "removed": removed,
            "failed": failed,
            "total_removed": len(removed),
            "status": "completed"
        }
    
    # Output JSON response to stdout
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()