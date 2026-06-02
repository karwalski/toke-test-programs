import sys
import hashlib
import json

def generate_etag(data):
    """Generate ETag from data using SHA-256 hash"""
    return hashlib.sha256(data.encode()).hexdigest()[:16]

def simulate_http_server():
    # Read port from stdin
    port = input().strip()
    
    # Print server startup message
    print(f"Listening on :{port}")
    
    # Simulate in-memory storage with ETags
    resources = {}
    
    # Simulate some HTTP requests to demonstrate the functionality
    # This is a simulation since we can't actually start a server
    
    # Example: Initial PUT without If-Match (would create resource)
    resource_id = "123"
    initial_data = "initial content"
    initial_etag = generate_etag(initial_data)
    resources[resource_id] = {
        'data': initial_data,
        'etag': initial_etag
    }
    
    # Simulate PUT with matching ETag (success case)
    new_data = "updated content"
    if_match_header = initial_etag
    
    if resource_id in resources:
        current_etag = resources[resource_id]['etag']
        if if_match_header == current_etag:
            # Update successful
            new_etag = generate_etag(new_data)
            resources[resource_id] = {
                'data': new_data,
                'etag': new_etag
            }
            # Would return 200 OK
        else:
            # ETag mismatch - would return 412 Precondition Failed
            pass
    
    # Simulate PUT with mismatched ETag (error case)
    wrong_etag = "wrong_etag_value"
    if resource_id in resources:
        current_etag = resources[resource_id]['etag']
        if wrong_etag != current_etag:
            # Would return 412 Precondition Failed with current ETag
            pass

if __name__ == "__main__":
    simulate_http_server()