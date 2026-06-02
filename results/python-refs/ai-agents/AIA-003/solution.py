import json
import sys

def validate_type(value, schema_type):
    if schema_type == "string":
        return isinstance(value, str)
    elif schema_type == "number":
        return isinstance(value, (int, float))
    elif schema_type == "integer":
        return isinstance(value, int)
    elif schema_type == "boolean":
        return isinstance(value, bool)
    elif schema_type == "array":
        return isinstance(value, list)
    elif schema_type == "object":
        return isinstance(value, dict)
    elif schema_type == "null":
        return value is None
    return False

def validate_schema(data, schema):
    errors = []
    
    # Check type
    if "type" in schema:
        if not validate_type(data, schema["type"]):
            errors.append(f"Expected type {schema['type']}, got {type(data).__name__}")
            return errors
    
    # For objects
    if isinstance(data, dict) and schema.get("type") == "object":
        # Check required properties
        if "required" in schema:
            for required_prop in schema["required"]:
                if required_prop not in data:
                    errors.append(f"Missing required property: {required_prop}")
        
        # Check properties
        if "properties" in schema:
            for prop_name, prop_value in data.items():
                if prop_name in schema["properties"]:
                    prop_schema = schema["properties"][prop_name]
                    prop_errors = validate_schema(prop_value, prop_schema)
                    for error in prop_errors:
                        errors.append(f"Property '{prop_name}': {error}")
    
    # Check enum constraint
    if "enum" in schema:
        if data not in schema["enum"]:
            errors.append(f"Value must be one of {schema['enum']}, got {data}")
    
    return errors

def main():
    input_data = json.loads(sys.stdin.read())
    schema = input_data["schema"]
    arguments = input_data["arguments"]
    
    errors = validate_schema(arguments, schema)
    
    result = {
        "valid": len(errors) == 0,
        "errors": errors
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()