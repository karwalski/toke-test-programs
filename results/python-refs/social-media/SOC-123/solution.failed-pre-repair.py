import json
import sys

def get_trending_posts(topic, limit):
    # Simulate a database of posts with engagement metrics
    all_posts = [
        {"id": 100, "content": "Just tried the new AI...", "author": "techie", "likes": 5000, "shares": 1200, "topic": "AI Release"},
        {"id": 101, "content": "Amazing AI breakthrough today!", "author": "researcher", "likes": 3500, "shares": 800, "topic": "AI Release"},
        {"id": 102, "content": "The future is here with this AI", "author": "futurist", "likes": 2800, "shares": 600, "topic": "AI Release"},
        {"id": 103, "content": "Climate change action needed now", "author": "activist", "likes": 4200, "shares": 1500, "topic": "Climate"},
        {"id": 104, "content": "New breakthrough in quantum computing", "author": "scientist", "likes": 1800, "shares": 400, "topic": "Tech"},
        {"id": 105, "content": "AI Release thoughts and opinions", "author": "blogger", "likes": 1200, "shares": 300, "topic": "AI Release"},
        {"id": 106, "content": "This AI Release is revolutionary", "author": "developer", "likes": 2200, "shares": 500, "topic": "AI Release"},
        {"id": 107, "content": "Sports update from the championship", "author": "sportsfan", "likes": 900, "shares": 200, "topic": "Sports"},
        {"id": 108, "content": "AI Release demo was incredible", "author": "youtuber", "likes": 1600, "shares": 350, "topic": "AI Release"},
        {"id": 109, "content": "Breaking: AI Release partnership announced", "author": "journalist", "likes": 3200, "shares": 700, "topic": "AI Release"}
    ]
    
    # Filter posts by topic
    topic_posts = [post for post in all_posts if post["topic"] == topic]
    
    # Calculate engagement score (likes + shares * 2 for weighted importance)
    for post in topic_posts:
        post["engagement_score"] = post["likes"] + (post["shares"] * 2)
    
    # Sort by engagement score in descending order
    topic_posts.sort(key=lambda x: x["engagement_score"], reverse=True)
    
    # Remove the helper fields and limit results
    result_posts = []
    for post in topic_posts[:limit]:
        result_post = {
            "id": post["id"],
            "content": post["content"],
            "author": post["author"],
            "likes": post["likes"],
            "shares": post["shares"]
        }
        result_posts.append(result_post)
    
    return result_posts

def main():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    request = json.loads(input_data)
    
    action = request.get("action")
    topic = request.get("topic")
    limit = request.get("limit", 10)
    
    if action == "trending_posts":
        posts = get_trending_posts(topic, limit)
        response = {
            "topic": topic,
            "posts": posts
        }
        print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()