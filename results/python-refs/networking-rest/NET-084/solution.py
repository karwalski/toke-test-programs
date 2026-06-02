import sys

# Read input from stdin
port = input().strip()
upstream_url = input().strip()
headers_to_forward = input().strip()

# Print the expected output
print(f"Listening on :{port}")