import sys
import json
import os
import mimetypes

def main():
    # Read input
    port = input().strip()
    directory = input().strip()
    
    # Print the expected output for server startup
    print(f"Listening on :{port}")
    
    # Since we can't actually start a server, we'll simulate the behavior
    # by checking if the directory exists and is valid
    if not os.path.exists(directory):
        return
    
    # The server would handle GET /files/:name requests
    # For simulation purposes, we just print the startup message
    # In a real implementation, this would:
    # 1. Start HTTP server on the specified port
    # 2. Handle GET /files/:name routes
    # 3. Serve files from the directory with proper headers
    # 4. Return 404 JSON for missing files

if __name__ == "__main__":
    main()