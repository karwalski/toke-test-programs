import json
import sys

# Mock data for demonstration
mock_comments = {
    1: [
        {"text": "Great post!", "is_top_level": True},
        {"text": "I agree", "is_top_level": False},
        {"text": "Nice work", "is_top_level": True},
        {"text": "Thanks", "is_top_level": False},
        {"text": "Cool", "is_top_level": True}
    ],
    2: [],
    3: [
        {"text": "Interesting", "is_top_level": True},
        {"text": "Reply 1", "is_top_level": False},
        {"text": "Reply 2", "is_top_level": False},
        {"text": "Another comment", "is_top_level": True},
        {"text": "Reply 3", "is_top_level": False},
        {"text": "Reply 4", "is_top_level": False},
        {"text": "Third comment", "is_top_level": True},
        {"text": "Reply 5", "is_top_level": False},
        {"text": "Reply 6", "is_top_level": False},
        {"text": "Reply 7", "is_top_level": False},
        {"text": "Reply 8", "is_top_level": False},
        {"text": "Fourth comment", "is_top_level": True}
    ]
}

def get_comment_data(post_id):
    comments = mock_comments.get(post_id, [])
    count = len(comments)
    
    # Find first top-level comment for preview
    preview = None
    for comment in comments:
        if comment.get("is_top_level", False):
            preview = comment["text"]
            break
    
    return count, preview

# Read input from stdin
input_data = json.loads(sys.stdin.read())

# Process the request
post_ids = input_data["post_ids"]
counts = []

for post_id in post_ids:
    count, preview = get_comment_data(post_id)
    counts.append({
        "post_id": post_id,
        "count": count,
        "preview": preview
    })

# Output response
response = {"counts": counts}
print(json.dumps(response, separators=(',', ':')))