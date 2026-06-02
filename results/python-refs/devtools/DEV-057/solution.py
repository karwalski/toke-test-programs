import json
import sys

def infer_type(value):
    if isinstance(value, bool):
        return "boolean"
    elif isinstance(value, int):
        return "integer"
    elif isinstance(value, float):
        return "number"
    elif isinstance(value, str):
        return "string"
    elif isinstance(value, list):
        return "array"
    elif isinstance(value, dict):
        return "object"
    elif value is None:
        return "null"
    else:
        return "string"

def infer_schema(data):
    if isinstance(data, dict):
        schema = {
            "type": "object",
            "properties": {},
            "required": []
        }
        
        for key in sorted(data.keys()):
            value = data[key]
            schema["properties"][key] = infer_schema(value)
            schema["required"].append(key)
        
        return schema
    
    elif isinstance(data, list):
        schema = {"type": "array"}
        if data:
            # Infer schema from first item
            schema["items"] = infer_schema(data[0])
        return schema
    
    else:
        return {"type": infer_type(data)}

# Read JSON from stdin
input_data = sys.stdin.read().strip()
data = json.loads(input_data)

# Infer schema
schema = infer_schema(data)

# Output schema as JSON
print(json.dumps(schema, separators=(',', ':')))