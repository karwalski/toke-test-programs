import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract data from input
    action = input_data["action"]
    token = input_data["token"]
    posts = input_data["posts"]
    
    # Create thread response
    thread_posts = []
    post_id = 5  # Starting ID as per expected output
    
    for i, post in enumerate(posts):
        thread_post = {
            "id": post_id + i,
            "content": post["content"],
            "position": i + 1
        }
        thread_posts.append(thread_post)
    
    # Create response object
    response = {
        "thread_id": "t1",
        "posts": thread_posts,
        "status": "created"
    }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()