import json
import sys

def convert_to_openai_schema(input_data):
    # Extract basic function info
    name = input_data["name"]
    description = input_data["description"]
    params = input_data["params"]
    
    # Build properties object
    properties = {}
    required = []
    
    for param in params:
        properties[param["name"]] = {
            "type": param["type"],
            "description": param["description"]
        }
        
        if param["required"]:
            required.append(param["name"])
    
    # Build the OpenAI schema
    schema = {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required
            }
        }
    }
    
    return schema

# Read input from stdin
input_text = sys.stdin.read().strip()
input_data = json.loads(input_text)

# Convert to OpenAI schema
output_schema = convert_to_openai_schema(input_data)

# Output JSON without extra whitespace
print(json.dumps(output_schema, separators=(',', ':')))