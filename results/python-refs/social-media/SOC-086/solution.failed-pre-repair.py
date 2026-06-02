import json
import sys

def main():
    # Read JSON input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Mock hashtag database with sample data
    hashtags_db = [
        {"tag": "programming", "post_count": 1500, "trending": True},
        {"tag": "productivity", "post_count": 800, "trending": False},
        {"tag": "progress", "post_count": 650, "trending": False},
        {"tag": "project", "post_count": 1200, "trending": True},
        {"tag": "professional", "post_count": 450, "trending": False}
    ]
    
    action = input_data.get("action")
    prefix = input_data.get("prefix", "")
    limit = input_data.get("limit", 10)
    
    if action == "search_hashtags":
        # Filter hashtags by prefix
        matching_hashtags = []
        for hashtag in hashtags_db:
            if hashtag["tag"].startswith(prefix.lower()):
                matching_hashtags.append({
                    "tag": hashtag["tag"],
                    "post_count": hashtag["post_count"],
                    "trending": hashtag["trending"]
                })
        
        # Sort by post_count descending and limit results
        matching_hashtags.sort(key=lambda x: x["post_count"], reverse=True)
        matching_hashtags = matching_hashtags[:limit]
        
        # Create response
        response = {"hashtags": matching_hashtags}
        
        # Output JSON response
        print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()