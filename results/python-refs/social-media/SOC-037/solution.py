import json
import sys

def main():
    # Read JSON input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract required fields
    action = input_data.get("action")
    token = input_data.get("token")
    list_id = input_data.get("list_id")
    cursor = input_data.get("cursor")
    
    # Simulate database of lists and posts
    lists_db = {
        "lst_1": {
            "name": "Tech People",
            "members": ["techie", "developer", "coder"]
        }
    }
    
    posts_db = [
        {"id": 20, "author": "techie", "content": "New framework"},
        {"id": 19, "author": "developer", "content": "Code review tips"},
        {"id": 18, "author": "other_user", "content": "Random post"}
    ]
    
    if action == "list_feed":
        # Get list info
        list_info = lists_db.get(list_id)
        if not list_info:
            response = {"error": "List not found"}
        else:
            # Filter posts by list members
            list_members = list_info["members"]
            filtered_posts = [
                post for post in posts_db 
                if post["author"] in list_members
            ]
            
            # For this example, return first post and no pagination
            response = {
                "list_id": list_id,
                "list_name": list_info["name"],
                "posts": filtered_posts[:1],  # Return first post only
                "next_cursor": None
            }
    else:
        response = {"error": "Unknown action"}
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()