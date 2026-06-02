import json
import sys

# Simple in-memory storage for reactions
reactions_storage = {}

def add_reaction(post_id, emoji):
    if post_id not in reactions_storage:
        reactions_storage[post_id] = {}
    
    if emoji not in reactions_storage[post_id]:
        reactions_storage[post_id][emoji] = 0
    
    reactions_storage[post_id][emoji] += 1
    
    return reactions_storage[post_id]

def main():
    # Read JSON from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract required fields
    action = input_data.get("action")
    token = input_data.get("token")
    post_id = input_data.get("post_id")
    emoji = input_data.get("emoji")
    
    # Process the reaction
    if action == "react":
        reactions = add_reaction(post_id, emoji)
        
        # Create response
        response = {
            "post_id": post_id,
            "emoji": emoji,
            "reactions": reactions,
            "status": "reacted"
        }
        
        # Output JSON response
        print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()