import json
import sys
import base64
import hmac
import hashlib
import time

def create_jwt_token(email, secret_key="my_secret_key", expires_in=3600):
    # JWT Header
    header = {
        "alg": "HS256",
        "typ": "JWT"
    }
    
    # JWT Payload
    current_time = int(time.time())
    payload = {
        "email": email,
        "exp": current_time + expires_in,
        "iat": current_time
    }
    
    # Encode header and payload
    def base64url_encode(data):
        json_str = json.dumps(data, separators=(',', ':'))
        encoded = base64.urlsafe_b64encode(json_str.encode()).decode()
        return encoded.rstrip('=')
    
    encoded_header = base64url_encode(header)
    encoded_payload = base64url_encode(payload)
    
    # Create signature
    message = f"{encoded_header}.{encoded_payload}"
    signature = hmac.new(
        secret_key.encode(),
        message.encode(),
        hashlib.sha256
    ).digest()
    
    encoded_signature = base64.urlsafe_b64encode(signature).decode().rstrip('=')
    
    # Combine all parts
    token = f"{encoded_header}.{encoded_payload}.{encoded_signature}"
    return token

def authenticate_user(email, password):
    # Simple user database simulation
    users = {
        "alice@example.com": "s3cur3!"
    }
    
    return users.get(email) == password

def main():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    request = json.loads(input_data)
    
    action = request.get("action")
    email = request.get("email")
    password = request.get("password")
    
    if action == "login":
        if authenticate_user(email, password):
            token = create_jwt_token(email)
            response = {
                "token": token,
                "expires_in": 3600,
                "status": "authenticated"
            }
        else:
            response = {
                "status": "failed",
                "message": "Invalid credentials"
            }
    else:
        response = {
            "status": "error",
            "message": "Invalid action"
        }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()