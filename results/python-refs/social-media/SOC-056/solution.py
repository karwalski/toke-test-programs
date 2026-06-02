import json
import sys

def get_post_metrics(post_id, token):
    # Mock engagement analytics data
    # In a real implementation, this would query a database or API
    mock_data = {
        1: {
            "post_id": 1,
            "views": 1000,
            "unique_views": 800,
            "likes": 50,
            "shares": 10,
            "link_clicks": 25,
            "profile_visits": 15,
            "reach": 1200
        }
    }
    
    return mock_data.get(post_id, {})

def main():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    
    try:
        # Parse JSON input
        request = json.loads(input_data)
        
        # Extract required fields
        action = request.get("action")
        token = request.get("token")
        post_id = request.get("post_id")
        
        # Validate action
        if action != "post_metrics":
            response = {"error": "Invalid action"}
        else:
            # Get metrics for the post
            response = get_post_metrics(post_id, token)
            
            if not response:
                response = {"error": "Post not found"}
    
    except json.JSONDecodeError:
        response = {"error": "Invalid JSON input"}
    except Exception as e:
        response = {"error": str(e)}
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()