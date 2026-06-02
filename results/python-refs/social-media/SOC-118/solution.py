import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Parse the request
    action = input_data.get("action")
    token = input_data.get("token")
    period = input_data.get("period")
    
    # Mock data for engagement rates by content type
    # In a real implementation, this would query a database using the token and period
    mock_engagement_data = [
        {"type": "image", "posts": 15, "avg_engagement_rate": 0.08},
        {"type": "text", "posts": 30, "avg_engagement_rate": 0.04},
        {"type": "poll", "posts": 3, "avg_engagement_rate": 0.12}
    ]
    
    # Create response
    response = {
        "types": mock_engagement_data
    }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()