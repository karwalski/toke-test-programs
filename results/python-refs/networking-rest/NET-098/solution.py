import sys
import json
import base64
import hmac
import hashlib
import secrets
import time
from urllib.parse import parse_qs, urlparse

def generate_jwt(payload, secret):
    # Simple JWT implementation using HS256
    header = {
        "alg": "HS256",
        "typ": "JWT"
    }
    
    # Base64URL encode header and payload
    def base64url_encode(data):
        json_str = json.dumps(data, separators=(',', ':'))
        encoded = base64.urlsafe_b64encode(json_str.encode()).decode()
        return encoded.rstrip('=')
    
    header_encoded = base64url_encode(header)
    payload_encoded = base64url_encode(payload)
    
    # Create signature
    message = f"{header_encoded}.{payload_encoded}"
    signature = hmac.new(
        secret.encode(),
        message.encode(),
        hashlib.sha256
    ).digest()
    signature_encoded = base64.urlsafe_b64encode(signature).decode().rstrip('=')
    
    return f"{message}.{signature_encoded}"

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    port = lines[0]
    client_id = lines[1]
    client_secret = lines[2]
    
    print(f"Listening on :{port}")
    
    # Simulate OAuth2 server behavior
    # This is a mock implementation that would handle:
    # 1. Authorization code flow
    # 2. Client credentials flow
    # 3. JWT token generation
    
    # Mock token generation for demonstration
    current_time = int(time.time())
    
    # Example access token payload
    access_token_payload = {
        "iss": "oauth2-server",
        "sub": client_id,
        "aud": "api",
        "exp": current_time + 3600,
        "iat": current_time,
        "scope": "read write"
    }
    
    access_token = generate_jwt(access_token_payload, client_secret)
    
    # Mock response format for client_credentials flow
    token_response = {
        "access_token": access_token,
        "token_type": "Bearer",
        "expires_in": 3600,
        "scope": "read write"
    }

if __name__ == "__main__":
    main()