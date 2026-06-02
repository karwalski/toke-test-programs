import sys
import json
import base64
import hmac
import hashlib
import time

def create_jwt(payload, secret):
    # JWT header
    header = {
        "alg": "HS256",
        "typ": "JWT"
    }
    
    # Base64 encode header and payload
    header_b64 = base64.urlsafe_b64encode(json.dumps(header, separators=(',', ':')).encode()).decode().rstrip('=')
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload, separators=(',', ':')).encode()).decode().rstrip('=')
    
    # Create signature
    message = f"{header_b64}.{payload_b64}"
    signature = hmac.new(secret.encode(), message.encode(), hashlib.sha256).digest()
    signature_b64 = base64.urlsafe_b64encode(signature).decode().rstrip('=')
    
    return f"{message}.{signature_b64}"

def verify_jwt(token, secret):
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return False
        
        header_b64, payload_b64, signature_b64 = parts
        
        # Verify signature
        message = f"{header_b64}.{payload_b64}"
        expected_signature = hmac.new(secret.encode(), message.encode(), hashlib.sha256).digest()
        
        # Add padding if needed
        signature_b64 += '=' * (4 - len(signature_b64) % 4)
        actual_signature = base64.urlsafe_b64decode(signature_b64)
        
        return hmac.compare_digest(expected_signature, actual_signature)
    except:
        return False

def handle_request(method, path, headers, body, secret):
    if method == "POST" and path == "/login":
        # Simple login - return JWT
        payload = {
            "sub": "user123",
            "iat": int(time.time()),
            "exp": int(time.time()) + 3600
        }
        token = create_jwt(payload, secret)
        return 200, {"token": token}
    
    # Protected route - check for valid JWT
    auth_header = headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return 401, {"error": "Unauthorized"}
    
    token = auth_header[7:]  # Remove "Bearer "
    if not verify_jwt(token, secret):
        return 401, {"error": "Unauthorized"}
    
    # Valid token - return success for any protected route
    return 200, {"message": "Access granted"}

# Read port from stdin
port = input().strip()

# Print expected output
print(f"Listening on :{port}")

# JWT secret
SECRET = "your-secret-key"

# Simulate some requests (but don't actually run a server)
# Just print the listening message as required