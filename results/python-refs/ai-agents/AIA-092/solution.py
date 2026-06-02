import json
import sys

def generate_rest_api_endpoints(data):
    model = data['model']
    operations = data['operations']
    model_name = model['name']
    model_fields = model['fields']
    
    endpoints = []
    
    # Determine plural form of model name for paths
    model_plural = model_name.lower() + 's'
    
    for operation in operations:
        if operation == 'list':
            endpoint = {
                "method": "GET",
                "path": f"/{model_plural}",
                "description": f"List all {model_plural}",
                "request_body": None,
                "response_schema": {
                    "type": "array",
                    "items": model_name
                }
            }
            endpoints.append(endpoint)
            
        elif operation == 'get':
            endpoint = {
                "method": "GET",
                "path": f"/{model_plural}/:id",
                "description": f"Get {model_name.lower()} by ID",
                "request_body": None,
                "response_schema": model_name
            }
            endpoints.append(endpoint)
            
        elif operation == 'create':
            # For create, exclude auto-generated fields like id and created_at
            request_fields = {}
            for field_name, field_type in model_fields.items():
                if field_name not in ['id', 'created_at']:
                    request_fields[field_name] = field_type
                    
            endpoint = {
                "method": "POST",
                "path": f"/{model_plural}",
                "description": f"Create a new {model_name.lower()}",
                "request_body": request_fields,
                "response_schema": model_name
            }
            endpoints.append(endpoint)
            
        elif operation == 'update':
            # For update, exclude auto-generated fields like id and created_at
            request_fields = {}
            for field_name, field_type in model_fields.items():
                if field_name not in ['id', 'created_at']:
                    request_fields[field_name] = field_type
                    
            endpoint = {
                "method": "PUT",
                "path": f"/{model_plural}/:id",
                "description": f"Update {model_name.lower()} by ID",
                "request_body": request_fields,
                "response_schema": model_name
            }
            endpoints.append(endpoint)
            
        elif operation == 'delete':
            endpoint = {
                "method": "DELETE",
                "path": f"/{model_plural}/:id",
                "description": f"Delete {model_name.lower()} by ID",
                "request_body": None,
                "response_schema": None
            }
            endpoints.append(endpoint)
    
    return endpoints

# Read input from stdin
input_data = json.loads(sys.stdin.read())

# Generate endpoints
endpoints = generate_rest_api_endpoints(input_data)

# Output JSON to stdout
print(json.dumps(endpoints, separators=(',', ':')))