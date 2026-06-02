import json
import sys
from datetime import datetime, timezone

def detect_viral_posts(threshold_multiplier):
    # Simulated post data with engagement metrics
    posts_data = [
        {
            "id": 15,
            "engagement_velocity": 500,
            "normal_velocity": 80,
            "peak_hour": "2026-01-01T14:00:00Z"
        },
        {
            "id": 12,
            "engagement_velocity": 120,
            "normal_velocity": 50,
            "peak_hour": "2026-01-01T12:00:00Z"
        },
        {
            "id": 8,
            "engagement_velocity": 200,
            "normal_velocity": 60,
            "peak_hour": "2026-01-01T10:00:00Z"
        }
    ]
    
    viral_posts = []
    
    for post in posts_data:
        multiplier = post["engagement_velocity"] / post["normal_velocity"]
        
        if multiplier >= threshold_multiplier:
            viral_posts.append({
                "id": post["id"],
                "engagement_velocity": post["engagement_velocity"],
                "normal_velocity": post["normal_velocity"],
                "multiplier": multiplier,
                "peak_hour": post["peak_hour"]
            })
    
    return viral_posts

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    action = input_data.get("action")
    threshold_multiplier = input_data.get("threshold_multiplier", 3)
    
    if action == "detect_viral":
        viral_posts = detect_viral_posts(threshold_multiplier)
        
        response = {
            "viral_posts": viral_posts
        }
        
        print(json.dumps(response, separators=(',', ':')))
    else:
        print(json.dumps({"error": "Unknown action"}, separators=(',', ':')))

if __name__ == "__main__":
    main()