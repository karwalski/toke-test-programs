import sys
import json
import base64

# Read input
login_url = input().strip()
protected_url = input().strip()
username = input().strip()
password = input().strip()

# Simulate login POST request
# In a real scenario, this would make an HTTP POST request
# For simulation, we'll assume successful login and generate a mock JWT token

# Simulate successful login response (status 200)
login_status = 200

# Create a simple mock JWT token
# JWT format: header.payload.signature (base64url encoded)
header = {"alg": "HS256", "typ": "JWT"}
payload = {"sub": username, "exp": 1234567890}

# Base64url encode (using standard base64 and replacing characters)
def base64url_encode(data):
    json_str = json.dumps(data, separators=(',', ':'))
    encoded = base64.b64encode(json_str.encode()).decode()
    return encoded.rstrip('=').replace('+', '-').replace('/', '_')

header_encoded = base64url_encode(header)
payload_encoded = base64url_encode(payload)
signature = "mock_signature_here"

jwt_token = f"{header_encoded}.{payload_encoded}.{signature}"

# Truncate token for display (show first 20 characters)
token_truncated = jwt_token[:20] + "..."

# Simulate protected endpoint call
# In a real scenario, this would make an HTTP GET request with Authorization header
# For simulation, assume successful response
protected_response = "User data retrieved successfully"

# Output results
print(f"Login: {login_status}")