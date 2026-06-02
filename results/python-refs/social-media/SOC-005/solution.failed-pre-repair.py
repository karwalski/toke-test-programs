import json
import sys
import hashlib
import hmac
import base64

# Simulated user database
users_db = {
    "user1": {
        "password_hash": hashlib.sha256("s3cur3!".encode()).hexdigest(),
        "token": "eyJ..."
    }
}

def verify_token(token):
    """Simulate token verification"""
    for username, user_data in users_db.items():
        if user_data["token"] == token:
            return username
    return None

def verify_password(username, password):
    """Verify user's current password"""
    if username in users_db:
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return users_db[username]["password_hash"] == password_hash
    return False

def change_password(username, new_password):
    """Change user's password"""
    new_password_hash = hashlib.sha256(new_password.encode()).hexdigest()
    users_db[username]["password_hash"] = new_password_hash

def main():
    try:
        # Read JSON input from stdin
        input_data = json.loads(sys.stdin.read().strip())
        
        action = input_data.get("action")
        token = input_data.get("token")
        old_password = input_data.get("old_password")
        new_password = input_data.get("new_password")
        
        if action != "change_password":
            print(json.dumps({"status": "invalid_action"}))
            return
        
        # Verify token and get username
        username = verify_token(token)
        if not username:
            print(json.dumps({"status": "invalid_token"}))
            return
        
        # Verify old password
        if not verify_password(username, old_password):
            print(json.dumps({"status": "invalid_old_password"}))
            return
        
        # Change password
        change_password(username, new_password)
        
        # Return success response
        print(json.dumps({"status": "password_changed"}))
        
    except (json.JSONDecodeError, KeyError):
        print(json.dumps({"status": "invalid_input"}))
    except Exception:
        print(json.dumps({"status": "error"}))

if __name__ == "__main__":
    main()