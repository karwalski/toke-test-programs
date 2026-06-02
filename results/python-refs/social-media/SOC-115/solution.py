import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Mock data for posts (simulating a database)
    posts_data = {
        1: {"impressions": 1000, "likes": 50, "shares": 10},
        5: {"impressions": 2000, "likes": 100, "shares": 25},
        10: {"impressions": 500, "likes": 20, "shares": 5}
    }
    
    # Extract post_ids from input
    post_ids = input_data["post_ids"]
    
    # Build comparison data
    comparison = []
    for post_id in post_ids:
        if post_id in posts_data:
            post_metrics = {
                "post_id": post_id,
                "impressions": posts_data[post_id]["impressions"],
                "likes": posts_data[post_id]["likes"],
                "shares": posts_data[post_id]["shares"]
            }
            comparison.append(post_metrics)
    
    # Create response
    response = {"comparison": comparison}
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()