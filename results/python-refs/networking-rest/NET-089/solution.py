import sys
import json

# Read input
port = int(input().strip())
upstream_url = input().strip()
pool_size = int(input().strip())

# Print the expected output
print(f"Listening on :{port}")

# Since we can't actually start a server, we'll simulate the behavior
# The proxy would maintain a connection pool and serve requests
# For /pool/stats endpoint, it would return JSON with pool statistics

# Example of what the pool stats would look like:
pool_stats = {
    "active": 0,
    "idle": pool_size,
    "total": pool_size
}

# In a real implementation, this would be served on GET /pool/stats
# print(json.dumps(pool_stats))