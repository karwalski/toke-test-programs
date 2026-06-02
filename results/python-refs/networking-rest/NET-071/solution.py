import json
import sys
from urllib.parse import urljoin

def create_hateoas_response(resource_id, base_url):
    """Create a HATEOAS-style JSON response for a resource"""
    resource = {
        "id": resource_id,
        "name": f"Resource {resource_id}",
        "_links": {
            "self": f"{base_url}/resources/{resource_id}",
            "edit": f"{base_url}/resources/{resource_id}/edit",
            "delete": f"{base_url}/resources/{resource_id}"
        }
    }
    return resource

def simulate_http_server(port):
    """Simulate HTTP server behavior without actually starting one"""
    base_url = f"http://localhost:{port}"
    
    # Print the server startup message
    print(f"Listening on :{port}")
    
    # Example of what the server would return for different endpoints
    # This demonstrates the HATEOAS JSON structure without running a real server
    
    # Example response for GET /resources/1
    example_resource = create_hateoas_response(1, base_url)
    
    # Example response for GET /resources (collection)
    collection_response = {
        "resources": [
            create_hateoas_response(1, base_url),
            create_hateoas_response(2, base_url),
            create_hateoas_response(3, base_url)
        ],
        "_links": {
            "self": f"{base_url}/resources",
            "create": f"{base_url}/resources/new"
        }
    }

if __name__ == "__main__":
    # Read port from stdin
    port = input().strip()
    
    # Simulate the HTTP server
    simulate_http_server(port)