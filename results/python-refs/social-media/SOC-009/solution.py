import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Simple token-to-email mapping for verification
token_map = {
    "tok_abc123": "alice@example.com"
}

# Process the verification request
if input_data.get("action") == "verify_email":
    token = input_data.get("verification_token")
    
    if token in token_map:
        response = {
            "status": "verified",
            "email": token_map[token]
        }
    else:
        response = {
            "status": "invalid",
            "error": "Invalid verification token"
        }
else:
    response = {
        "status": "error",
        "error": "Invalid action"
    }

# Output JSON response
print(json.dumps(response, separators=(',', ':')))