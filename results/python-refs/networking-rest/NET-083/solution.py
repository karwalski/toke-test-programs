import sys
import json
from datetime import datetime
from urllib.parse import urlparse, parse_qs

# Read port from stdin
port = int(input().strip())

# Print the expected output
print(f"Listening on :{port}")

# Simulate the HTTP server behavior
class ResourceServer:
    def __init__(self):
        self.resources = {}
        self.next_id = 1
    
    def handle_request(self, method, path, query_params=None):
        if query_params is None:
            query_params = {}
            
        if method == "GET" and path == "/resources":
            include_deleted = query_params.get("include_deleted", ["false"])[0].lower() == "true"
            result = []
            
            for resource_id, resource in self.resources.items():
                if include_deleted or resource.get("deletedAt") is None:
                    result.append({
                        "id": resource_id,
                        "data": resource.get("data", {}),
                        "deletedAt": resource.get("deletedAt")
                    })
            
            return {"status": 200, "body": result}
        
        elif method == "GET" and path.startswith("/resources/"):
            resource_id = path.split("/")[-1]
            
            if resource_id not in self.resources:
                return {"status": 404, "body": {"error": "Resource not found"}}
            
            resource = self.resources[resource_id]
            if resource.get("deletedAt") is not None:
                return {"status": 404, "body": {"error": "Resource not found"}}
            
            return {"status": 200, "body": {
                "id": resource_id,
                "data": resource.get("data", {}),
                "deletedAt": resource.get("deletedAt")
            }}
        
        elif method == "POST" and path == "/resources":
            resource_id = str(self.next_id)
            self.next_id += 1
            
            self.resources[resource_id] = {
                "data": {},
                "deletedAt": None
            }
            
            return {"status": 201, "body": {
                "id": resource_id,
                "data": {},
                "deletedAt": None
            }}
        
        elif method == "DELETE" and path.startswith("/resources/"):
            resource_id = path.split("/")[-1]
            
            if resource_id not in self.resources:
                return {"status": 404, "body": {"error": "Resource not found"}}
            
            resource = self.resources[resource_id]
            if resource.get("deletedAt") is not None:
                return {"status": 404, "body": {"error": "Resource not found"}}
            
            # Perform soft delete
            self.resources[resource_id]["deletedAt"] = datetime.utcnow().isoformat() + "Z"
            
            return {"status": 204, "body": None}
        
        else:
            return {"status": 404, "body": {"error": "Not found"}}

# Create server instance (simulation only)
server = ResourceServer()