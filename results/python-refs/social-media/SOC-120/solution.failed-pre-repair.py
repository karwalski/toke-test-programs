import json
import sys

def get_trending_topics(region, limit):
    # Simulated trending topics data
    all_topics = [
        {"rank": 1, "name": "World Cup", "post_count": 25000, "velocity": 500, "category": "sports"},
        {"rank": 2, "name": "AI Release", "post_count": 18000, "velocity": 350, "category": "technology"},
        {"rank": 3, "name": "Climate Summit", "post_count": 15000, "velocity": 300, "category": "politics"},
        {"rank": 4, "name": "New Movie", "post_count": 12000, "velocity": 250, "category": "entertainment"},
        {"rank": 5, "name": "Stock Market", "post_count": 10000, "velocity": 200, "category": "finance"},
        {"rank": 6, "name": "Space Mission", "post_count": 8000, "velocity": 180, "category": "science"},
        {"rank": 7, "name": "Fashion Week", "post_count": 7000, "velocity": 150, "category": "lifestyle"},
        {"rank": 8, "name": "Gaming News", "post_count": 6500, "velocity": 140, "category": "gaming"},
        {"rank": 9, "name": "Health Study", "post_count": 6000, "velocity": 120, "category": "health"},
        {"rank": 10, "name": "Music Awards", "post_count": 5500, "velocity": 100, "category": "entertainment"}
    ]
    
    # Return topics limited by the requested limit
    return all_topics[:limit]

def main():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    request = json.loads(input_data)
    
    action = request.get("action")
    region = request.get("region", "global")
    limit = request.get("limit", 10)
    
    if action == "trending_topics":
        topics = get_trending_topics(region, limit)
        response = {"topics": topics}
        
        # Output JSON response to stdout
        print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()