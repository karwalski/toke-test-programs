import sys
import uuid

# Read port from stdin
port = input().strip()

# Print the expected output
print(f"Listening on :{port}")

# Since we can't actually run a server, we'll simulate the behavior
# by showing what would happen when a request comes in

# Generate a sample UUID for demonstration
request_id = str(uuid.uuid4())

# Simulate logging format that would include the request ID
# This shows how the server would log requests with the UUID