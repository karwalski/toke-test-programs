import json
import sys

def main():
    # Read JSON input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract parameters
    action = input_data.get("action")
    period = input_data.get("period")
    limit = input_data.get("limit")
    
    # Simulate trending hashtags data based on the input
    if action == "trending_hashtags":
        # Mock data that matches the expected output format
        hashtags = [
            {"tag": "breaking", "posts_24h": 5000, "growth_rate": 2.5},
            {"tag": "newrelease", "posts_24h": 3000, "growth_rate": 1.8}
        ]
        
        # Limit the results based on the limit parameter
        if limit and len(hashtags) > limit:
            hashtags = hashtags[:limit]
        
        # Create response
        response = {"hashtags": hashtags}
        
        # Output JSON response to stdout
        print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()