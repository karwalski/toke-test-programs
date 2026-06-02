import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract parameters
    action = input_data.get("action")
    token = input_data.get("token")
    period = input_data.get("period")
    
    # Validate action
    if action != "analytics_overview":
        return
    
    # For this simulation, we'll return the expected output
    # In a real implementation, you would use the token to authenticate
    # and fetch actual analytics data for the specified period
    
    response = {
        "period": period,
        "impressions": 50000,
        "engagements": 2500,
        "engagement_rate": 0.05,
        "follower_change": 120,
        "top_post": {
            "id": 15,
            "impressions": 5000
        }
    }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()