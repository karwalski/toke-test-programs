import json
import sys

def main():
    input_data = json.loads(sys.stdin.read().strip())
    
    users_db = [
        {"id": 1, "username": "alice", "verified": False, "followers": 500, "bio": "Web developer", "location": "NYC"},
        {"id": 2, "username": "bob", "verified": True, "followers": 2500, "bio": "Mobile developer", "location": "SF"},
        {"id": 3, "username": "charlie", "verified": False, "followers": 150, "bio": "Student developer", "location": "LA"},
        {"id": 10, "username": "topdev", "verified": True, "followers": 5000, "bio": "Senior developer", "location": "Seattle"},
        {"id": 4, "username": "diana", "verified": True, "followers": 800, "bio": "Designer and developer", "location": "Austin"},
        {"id": 5, "username": "eve", "verified": False, "followers": 1200, "bio": "Backend developer", "location": "NYC"}
    ]
    
    action = input_data.get("action")
    query = input_data.get("query", "")
    filters = input_data.get("filters", {})
    
    if action == "search_users_filtered":
        filtered_users = users_db[:]
        
        if "verified" in filters:
            verified = filters["verified"]
            filtered_users = [u for u in filtered_users if u["verified"] == verified]
        
        if "min_followers" in filters:
            mf = filters["min_followers"]
            filtered_users = [u for u in filtered_users if u["followers"] >= mf]
        
        if "max_followers" in filters:
            mf = filters["max_followers"]
            filtered_users = [u for u in filtered_users if u["followers"] <= mf]
        
        if "location" in filters:
            loc = filters["location"]
            filtered_users = [u for u in filtered_users if u["location"] == loc]
        
        response_users = []
        for u in filtered_users:
            response_users.append({
                "id": u["id"],
                "username": u["username"],
                "verified": u["verified"],
                "followers": u["followers"],
                "bio": u["bio"]
            })
        
        response = {"users": response_users, "total": len(response_users)}
        print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()