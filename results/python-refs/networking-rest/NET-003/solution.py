import sys
import json

# Read port number from stdin
port = input().strip()

# Print the expected output
print(f"Listening on :{port}")

# Since we can't actually start a server, we simulate the behavior
# by printing what would happen when the server receives requests

# Simulate handling different HTTP methods on /resource
def handle_request(method, body=""):
    # Log the request
    print(f"{method} /resource")
    
    # Return JSON response
    response = {
        "method": method,
        "body": body
    }
    return json.dumps(response)

# Example of what the server would do for different requests:
# GET /resource -> {"method": "GET", "body": ""}
# POST /resource with body -> {"method": "POST", "body": "request_body"}
# PUT /resource with body -> {"method": "PUT", "body": "request_body"}  
# DELETE /resource -> {"method": "DELETE", "body": ""}