import json
import sys

# Mock data structure for comments
comments_db = {
    1: {"id": 1, "content": "Great post!", "author": "alice", "parent_id": None},
    2: {"id": 2, "content": "Thanks!", "author": "bob", "parent_id": 1}
}

def get_replies(comment_id):
    replies = []
    for cid, comment in comments_db.items():
        if comment.get("parent_id") == comment_id:
            reply = {
                "id": comment["id"],
                "content": comment["content"],
                "author": comment["author"],
                "replies": get_replies(comment["id"])
            }
            replies.append(reply)
    return replies

def get_thread(comment_id):
    if comment_id not in comments_db:
        return None
    
    root_comment = comments_db[comment_id]
    thread = {
        "id": root_comment["id"],
        "content": root_comment["content"],
        "author": root_comment["author"],
        "replies": get_replies(comment_id)
    }
    
    return {"root": thread}

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

if input_data["action"] == "get_thread":
    result = get_thread(input_data["comment_id"])
    print(json.dumps(result, separators=(',', ':')))