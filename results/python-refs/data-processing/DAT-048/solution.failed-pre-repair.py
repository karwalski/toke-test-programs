import json
import sys

def infer_type(value):
    """Infer the JSON schema type for a value."""
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

def merge_schemas(schema1, schema2):
    """Merge two schemas together."""
    if schema1 is None:
        return schema2
    if schema2 is None:
        return schema1
    
    # If types are different, we need to handle this
    if schema1.get("type") != schema2.get("type"):
        # For simplicity, if types differ, we'll use the first one
        # In a more complete implementation, we might use "anyOf"
        return schema1
    
    merged = {"type": schema1["type"]}
    
    if schema1["type"] == "integer" or schema1["type"] == "number":
        # Merge numeric constraints
        if "minimum" in schema1 and "minimum" in schema2:
            merged["minimum"] = min(schema1["minimum"], schema2["minimum"])
        elif "minimum" in schema1:
            merged["minimum"] = schema1["minimum"]
        elif "minimum" in schema2:
            merged["minimum"] = schema2["minimum"]
            
        if "maximum" in schema1 and "maximum" in schema2:
            merged["maximum"] = max(schema1["maximum"], schema2["maximum"])
        elif "maximum" in schema1:
            merged["maximum"] = schema1["maximum"]
        elif "maximum" in schema2:
            merged["maximum"] = schema2["maximum"]
    
    elif schema1["type"] == "object":
        # Merge object properties
        props1 = schema1.get("properties", {})
        props2 = schema2.get("properties", {})
        merged_props = {}
        
        all_keys = set(props1.keys()) | set(props2.keys())
        for key in all_keys:
            if key in props1 and key in props2:
                merged_props[key] = merge_schemas(props1[key], props2[key])
            elif key in props1:
                merged_props[key] = props1[key]
            else:
                merged_props[key] = props2[key]
        
        merged["properties"] = merged_props
        
        # Merge required fields (intersection - only fields present in all objects)
        req1 = set(schema1.get("required", []))
        req2 = set(schema2.get("required", []))
        required = req1 & req2
        if required:
            merged["required"] = sorted(list(required))
    
    return merged

def infer_schema_from_value(value):
    """Infer schema from a single value."""
    value_type = infer_type(value)
    schema = {"type": value_type}
    
    if value_type == "integer" or value_type == "number":
        schema["minimum"] = value
        schema["maximum"] = value
    elif value_type == "object":
        properties = {}
        for key, val in value.items():
            properties[key] = infer_schema_from_value(val)
        schema["properties"] = properties
        schema["required"] = sorted(list(value.keys()))
    elif value_type == "array":
        # For arrays, we'd need to infer item schema
        schema["items"] = {}
    
    return schema

def main():
    objects = []
    
    # Read JSON objects from stdin
    for line in sys.stdin:
        line = line.strip()
        if line:
            try:
                obj = json.loads(line)
                objects.append(obj)
            except json.JSONDecodeError:
                continue
    
    if not objects:
        return
    
    # Infer schema from all objects
    merged_schema = None
    for obj in objects:
        obj_schema = infer_schema_from_value(obj)
        merged_schema = merge_schemas(merged_schema, obj_schema)
    
    # Output the schema with exact formatting
    print(json.dumps(merged_schema, indent=2, separators=(',', ': ')))

if __name__ == "__main__":
    main()