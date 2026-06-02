import json
import sys

def main():
    # Read JSON input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Mock user database
    users_db = [
        {"id": 1, "username": "alice", "verified": False, "followers": 500, "bio": "Web developer", "location": "NYC"},
        {"id": 2, "username": "bob", "verified": True, "followers": 2500, "bio": "Mobile developer", "location": "SF"},
        {"id": 3, "username": "charlie", "verified": False, "followers": 150, "bio": "Student developer", "location": "LA"},
        {"id": 10, "username": "topdev", "verified": True, "followers": 5000, "bio": "Senior developer", "location": "Seattle"},
        {"id": 4, "username": "diana", "verified": True, "followers": 800, "bio": "Designer and developer", "location": "Austin"},
        {"id": 5, "username": "eve", "verified": False, "followers": 1200, "bio": "Backend developer", "location": "NYC"}
    ]
    
    # Extract query and filters
    action = input_data.get("action")
    query = input_data.get("query", "")
    filters = input_data.get("filters", {})
    
    if action == "search_users_filtered":
        # Start with all users
        filtered_users = users_db[:]
        
        # Apply text query filter (search in username and bio)
        if query:
            query_lower = query.lower()
            filtered_users = [user for user in filtered_users 
                            if query_lower in user["username"].lower() or 
                               query_lower in user["bio"].lower()]
        
        # Apply verified status filter
        if "verified" in filters:
            verified = filters["verified"]
            filtered_users = [user for user in filtered_users if user["verified"] == verified]
        
        # Apply minimum followers filter
        if "min_followers" in filters:
            min_followers = filters["min_followers"]
            filtered_users = [user for user in filtered_users if user["followers"] >= min_followers]
        
        # Apply maximum followers filter
        if "max_followers" in filters:
            max_followers = filters["max_followers"]
            filtered_users = [user for user in filtered_users if user["followers"] <= max_followers]
        
        # Apply location filter
        if "location" in filters:
            location = filters["location"]
            filtered_users = [user for user in filtered_users if user["location"] == location]
        
        # Prepare response format (remove location from output)
        response_users = []
        for user in filtered_users:
            response_user = {
                "id": user["id"],
                "username": user["username"],
                "verified": user["verified"],
                "followers": user["followers"],
                "bio": user["bio"]
            }
            response_users.append(response_user)
        
        response = {
            "users": response_users,
            "total": len(response_users)
        }
        
        # Output JSON response
        print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()