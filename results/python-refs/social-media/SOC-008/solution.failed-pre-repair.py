import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Mock user database
    users_db = [
        {"id": 1, "username": "alice"},
        {"id": 2, "username": "bob"},
        {"id": 3, "username": "charlie"},
        {"id": 4, "username": "david"},
        {"id": 5, "username": "alice_smith"},
        {"id": 6, "username": "alison"},
        {"id": 7, "username": "malice"}
    ]
    
    action = input_data.get("action")
    
    if action == "search_users":
        query = input_data.get("query", "").lower()
        page = input_data.get("page", 1)
        limit = input_data.get("limit", 10)
        
        # Filter users by partial username match
        matched_users = []
        for user in users_db:
            if query in user["username"].lower():
                matched_users.append(user)
        
        # Calculate pagination
        total = len(matched_users)
        start_index = (page - 1) * limit
        end_index = start_index + limit
        
        # Get paginated results
        paginated_users = matched_users[start_index:end_index]
        
        # Check if there's a next page
        has_next = end_index < total
        
        # Create response
        response = {
            "users": paginated_users,
            "total": total,
            "page": page,
            "has_next": has_next
        }
        
        # Output JSON response
        print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()