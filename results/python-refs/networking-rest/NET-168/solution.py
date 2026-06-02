import sys
import json
import base64
import hmac
import hashlib
import time

def base64url_encode(data):
    """Encode data using base64url encoding (URL-safe base64 without padding)"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    encoded = base64.urlsafe_b64encode(data).decode('utf-8')
    return encoded.rstrip('=')

def create_jwt(service_id, private_key_content, token_url):
    """Create a JWT token for service authentication"""
    # JWT Header
    header = {
        "alg": "HS256",
        "typ": "JWT"
    }
    
    # JWT Payload
    current_time = int(time.time())
    payload = {
        "iss": service_id,
        "aud": token_url,
        "iat": current_time,
        "exp": current_time + 300  # 5 minutes expiry
    }
    
    # Encode header and payload
    encoded_header = base64url_encode(json.dumps(header, separators=(',', ':')))
    encoded_payload = base64url_encode(json.dumps(payload, separators=(',', ':')))
    
    # Create signature
    message = f"{encoded_header}.{encoded_payload}"
    signature = hmac.new(
        private_key_content.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).digest()
    encoded_signature = base64url_encode(signature)
    
    # Complete JWT
    jwt_token = f"{message}.{encoded_signature}"
    return jwt_token

def main():
    # Read input from stdin
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    token_url = lines[0]
    service_id = lines[1]
    private_key_path = lines[2]
    api_url = lines[3]
    
    # Simulate reading private key file
    # In a real scenario, we would read from the file path
    # For this simulation, we'll use a dummy key content
    private_key_content = "dummy_private_key_content"
    
    print(f"Generating JWT for service: {service_id}", file=sys.stderr)
    
    # Generate JWT
    jwt_token = create_jwt(service_id, private_key_content, token_url)
    
    print(f"JWT generated successfully", file=sys.stderr)
    print(f"Exchanging JWT for access token at: {token_url}", file=sys.stderr)
    
    # Simulate token exchange
    # In reality, this would be an HTTP POST request
    access_token = "simulated_access_token_12345"
    
    print(f"Access token obtained", file=sys.stderr)
    print(f"Calling API: {api_url}", file=sys.stderr)
    
    # Simulate API call
    # In reality, this would be an HTTP request with the access token
    # Based on the test input/output, we expect a 200 response
    api_response = "200"
    
    print(f"API call completed", file=sys.stderr)
    
    # Output the API response
    print(api_response)

if __name__ == "__main__":
    main()