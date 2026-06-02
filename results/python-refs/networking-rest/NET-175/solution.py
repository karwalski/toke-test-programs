import sys
import urllib.request
import json

def infer_json_schema(data):
    """Infer JSON schema from data structure"""
    if data is None:
        return {"type": "null"}
    
    if isinstance(data, bool):
        return {"type": "boolean"}
    
    if isinstance(data, int):
        return {"type": "integer"}
    
    if isinstance(data, float):
        return {"type": "number"}
    
    if isinstance(data, str):
        return {"type": "string"}
    
    if isinstance(data, list):
        if not data:
            return {"type": "array", "items": {}}
        
        # Infer schema from first item (simplified approach)
        item_schema = infer_json_schema(data[0])
        return {"type": "array", "items": item_schema}
    
    if isinstance(data, dict):
        schema = {
            "type": "object",
            "properties": {},
            "required": []
        }
        
        for key, value in data.items():
            schema["properties"][key] = infer_json_schema(value)
            # Assume all properties are required for simplicity
            schema["required"].append(key)
        
        return schema
    
    return {"type": "string"}  # fallback

def main():
    urls = []
    for line in sys.stdin:
        url = line.strip()
        if url:
            urls.append(url)
    
    for url in urls:
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode('utf-8'))
                schema = infer_json_schema(data)
                print(json.dumps(schema, indent=2))
        except Exception:
            # If there's an error, output a basic schema
            print(json.dumps({"type": "object"}, indent=2))

if __name__ == "__main__":
    main()