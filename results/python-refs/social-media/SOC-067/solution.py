import json
import sys

def main():
    # Read JSON input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract required fields
    action = input_data.get("action")
    token = input_data.get("token")
    post_id = input_data.get("post_id")
    allowed = input_data.get("allowed")
    
    # Validate action
    if action == "set_comment_policy":
        # Validate allowed values
        valid_policies = ["everyone", "followers", "mentioned", "nobody"]
        if allowed in valid_policies:
            # Create response
            response = {
                "post_id": post_id,
                "comment_policy": allowed,
                "status": "updated"
            }
        else:
            response = {
                "error": "invalid_policy"
            }
    else:
        response = {
            "error": "invalid_action"
        }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()