import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract parameters
    action = input_data.get("action")
    token = input_data.get("token")
    period = input_data.get("period")
    
    # Mock hashtag performance data
    hashtag_data = [
        {
            "tag": "programming",
            "uses": 10,
            "avg_impressions": 2000,
            "avg_engagement": 100
        },
        {
            "tag": "rust",
            "uses": 5,
            "avg_impressions": 1500,
            "avg_engagement": 80
        }
    ]
    
    # Create response
    response = {
        "hashtags": hashtag_data
    }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()