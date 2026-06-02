import sys
import random

# Read port number from stdin
port = int(input().strip())

# Print the expected output
print(f"Listening on :{port}")

# Simulate Server-Timing header generation for demonstration
# In a real HTTP server, this would be included in response headers
# Format: Server-Timing: db;dur=23.2, cache;dur=5.1, render;dur=12.8

# Generate random timing values to simulate the phases
db_time = round(random.uniform(10.0, 50.0), 1)
cache_time = round(random.uniform(1.0, 15.0), 1)
render_time = round(random.uniform(5.0, 25.0), 1)

# Example of what the Server-Timing header would look like
server_timing = f"Server-Timing: db;dur={db_time}, cache;dur={cache_time}, render;dur={render_time}"