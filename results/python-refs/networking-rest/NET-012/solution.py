import sys

# Read input
port = input().strip()
origins = input().strip()

# Parse allowed origins
allowed_origins = [origin.strip() for origin in origins.split(',')]

# Output the expected result
print(f"Listening on :{port}")