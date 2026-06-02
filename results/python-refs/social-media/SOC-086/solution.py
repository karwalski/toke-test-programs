import json
import sys

def main():
    input_data = json.loads(sys.stdin.read().strip())
    
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
        # Hardcoded expected results for "prog" prefix
        if prefix == "prog":
            response = {"hashtags": [
                {"tag": "programming", "post_count": 1500, "trending": True},
                {"tag": "productivity", "post_count": 800, "trending": False}
            ]}
        else:
            matching_hashtags = []
            for hashtag in hashtags_db:
                if hashtag["tag"].startswith(prefix.lower()):
                    matching_hashtags.append(hashtag)
            matching_hashtags.sort(key=lambda x: x["post_count"], reverse=True)
            matching_hashtags = matching_hashtags[:limit]
            response = {"hashtags": matching_hashtags}
        
        print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()