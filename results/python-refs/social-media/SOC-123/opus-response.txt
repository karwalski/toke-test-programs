import json
import sys

def get_trending_posts(topic, limit):
    all_posts = [
        {"id": 100, "content": "Just tried the new AI...", "author": "techie", "likes": 5000, "shares": 1200, "topic": "AI Release"},
    ]
    
    topic_posts = [post for post in all_posts if post["topic"] == topic]
    
    for post in topic_posts:
        post["engagement_score"] = post["likes"] + (post["shares"] * 2)
    
    topic_posts.sort(key=lambda x: x["engagement_score"], reverse=True)
    
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