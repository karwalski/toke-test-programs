import json
import sys
from collections import deque

def get_follow_graph():
    # Sample follow graph - in a real implementation this would come from a database
    users = {
        1: {"id": 1, "username": "alice"},
        2: {"id": 2, "username": "bob"},
        3: {"id": 3, "username": "charlie"},
        4: {"id": 4, "username": "diana"},
        5: {"id": 5, "username": "eve"},
        6: {"id": 6, "username": "fred"},
        7: {"id": 7, "username": "grace"},
        8: {"id": 8, "username": "henry"},
        9: {"id": 9, "username": "iris"},
        10: {"id": 10, "username": "frank"}
    }
    
    # Follow relationships (adjacency list)
    follows = {
        1: [2, 5],
        2: [3, 4],
        3: [6],
        4: [7],
        5: [8, 10],
        6: [9],
        7: [8],
        8: [9],
        9: [10],
        10: []
    }
    
    return users, follows

def find_shortest_path(users, follows, user_id_a, user_id_b, max_depth):
    if user_id_a == user_id_b:
        return 0, [users[user_id_a]]
    
    if user_id_a not in users or user_id_b not in users:
        return None, []
    
    # BFS to find shortest path
    queue = deque([(user_id_a, [user_id_a])])
    visited = {user_id_a}
    
    while queue:
        current_user, path = queue.popleft()
        
        if len(path) - 1 >= max_depth:
            continue
            
        for neighbor in follows.get(current_user, []):
            if neighbor == user_id_b:
                final_path = path + [neighbor]
                user_path = [users[uid] for uid in final_path]
                return len(final_path) - 1, user_path
            
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    return None, []

def main():
    input_data = json.loads(sys.stdin.read().strip())
    
    action = input_data["action"]
    user_id_a = input_data["user_id_a"]
    user_id_b = input_data["user_id_b"]
    max_depth = input_data["max_depth"]
    
    users, follows = get_follow_graph()
    
    distance, path = find_shortest_path(users, follows, user_id_a, user_id_b, max_depth)
    
    if distance is not None:
        response = {
            "distance": distance,
            "path": path,
            "status": "found"
        }
    else:
        response = {
            "distance": -1,
            "path": [],
            "status": "not_found"
        }
    
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()