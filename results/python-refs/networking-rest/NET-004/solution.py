import sys
import json
from urllib.parse import urlparse, parse_qs

# Read port from stdin
port = input().strip()

# In-memory storage for users
users = {}
next_user_id = 1

def log_operation(method, path, status_code, response_data=None):
    """Log each operation"""
    log_entry = f"{method} {path} -> {status_code}"
    if response_data:
        log_entry += f" {json.dumps(response_data)}"
    print(log_entry, file=sys.stderr)

def handle_get_users():
    """Handle GET /users"""
    user_list = list(users.values())
    log_operation("GET", "/users", 200, user_list)
    return {"status": 200, "data": user_list}

def handle_post_users(body):
    """Handle POST /users"""
    global next_user_id
    try:
        user_data = json.loads(body)
        user_data["id"] = next_user_id
        users[next_user_id] = user_data
        next_user_id += 1
        log_operation("POST", "/users", 201, user_data)
        return {"status": 201, "data": user_data}
    except json.JSONDecodeError:
        log_operation("POST", "/users", 400, {"error": "Invalid JSON"})
        return {"status": 400, "data": {"error": "Invalid JSON"}}

def handle_get_user(user_id):
    """Handle GET /users/:id"""
    if user_id in users:
        user_data = users[user_id]
        log_operation("GET", f"/users/{user_id}", 200, user_data)
        return {"status": 200, "data": user_data}
    else:
        error_data = {"error": "User not found"}
        log_operation("GET", f"/users/{user_id}", 404, error_data)
        return {"status": 404, "data": error_data}

def handle_put_user(user_id, body):
    """Handle PUT /users/:id"""
    try:
        user_data = json.loads(body)
        user_data["id"] = user_id
        users[user_id] = user_data
        log_operation("PUT", f"/users/{user_id}", 200, user_data)
        return {"status": 200, "data": user_data}
    except json.JSONDecodeError:
        error_data = {"error": "Invalid JSON"}
        log_operation("PUT", f"/users/{user_id}", 400, error_data)
        return {"status": 400, "data": error_data}

def handle_delete_user(user_id):
    """Handle DELETE /users/:id"""
    if user_id in users:
        del users[user_id]
        success_data = {"message": "User deleted"}
        log_operation("DELETE", f"/users/{user_id}", 200, success_data)
        return {"status": 200, "data": success_data}
    else:
        error_data = {"error": "User not found"}
        log_operation("DELETE", f"/users/{user_id}", 404, error_data)
        return {"status": 404, "data": error_data}

def route_request(method, path, body=""):
    """Route requests to appropriate handlers"""
    path_parts = path.strip('/').split('/')
    
    if path == "/users":
        if method == "GET":
            return handle_get_users()
        elif method == "POST":
            return handle_post_users(body)
    elif len(path_parts) == 2 and path_parts[0] == "users":
        try:
            user_id = int(path_parts[1])
            if method == "GET":
                return handle_get_user(user_id)
            elif method == "PUT":
                return handle_put_user(user_id, body)
            elif method == "DELETE":
                return handle_delete_user(user_id)
        except ValueError:
            pass
    
    # 404 for unmatched routes
    error_data = {"error": "Not found"}
    log_operation(method, path, 404, error_data)
    return {"status": 404, "data": error_data}

# Print the expected output
print(f"Listening on :{port}")