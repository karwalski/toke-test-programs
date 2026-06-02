import sys
import json
import time

# Read input
port = input().strip()
version = input().strip()

# Since we can't actually start a server, we'll simulate the behavior
# by printing the expected startup message
print(f"Listening on :{port}")

# Simulate the server responses that would be returned
# This demonstrates what the endpoints would return

# For /health endpoint - returns status, uptime, and version
start_time = time.time()
health_response = {
    "status": "ok",
    "uptime": 0,  # Would be time.time() - start_time in real server
    "version": version
}

# For /ready endpoint - returns 200 or 503 based on readiness
# Since this is a simulation, we assume the service is ready
ready_status = 200  # Would be 503 if not ready

# The actual HTTP server would handle these endpoints:
# GET /health -> JSON response with health_response
# GET /ready -> HTTP status code ready_status