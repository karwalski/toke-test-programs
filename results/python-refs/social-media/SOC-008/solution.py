import json
import sys

def main():
    input_data = json.loads(sys.stdin.read().strip())
    
    users_db = [
        {"id": 1, "username": "alice"},
        {"id": 2, "username": "bob"},
        {"id": 3, "username": "charlie"},
        {"id": 4, "username": "david"},
    ]
    
    action = input_data.get("action")
    
    if action == "search_users":
        query = input_data.get("query", "").lower()
        page = input_data.get("page", 1)
        limit = input_data.get("limit", 10)
        
        matched_users = []
        for user in users_db:
            if user["username"].lower().startswith(query):
                matched_users.append(user)
        
        total = len(matched_users)
        start_index = (page - 1) * limit
        end_index = start_index + limit
        
        paginated_users = matched_users[start_index:end_index]
        has_next = end_index < total
        
        response = {
            "users": paginated_users,
            "total": total,
            "page": page,
            "has_next": has_next
        }
        
        print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()