import sys
import json
import re

def validate_type(value, expected_type):
    if expected_type == "string":
        return isinstance(value, str)
    elif expected_type == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    elif expected_type == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    elif expected_type == "boolean":
        return isinstance(value, bool)
    elif expected_type == "array":
        return isinstance(value, list)
    elif expected_type == "object":
        return isinstance(value, dict)
    elif expected_type == "null":
        return value is None
    return False

def validate_value(value, schema, path=""):
    errors = []
    
    # Type validation
    if "type" in schema:
        if not validate_type(value, schema["type"]):
            errors.append(f"Type mismatch at {path or 'root'}: expected {schema['type']}")
    
    # String pattern validation
    if "pattern" in schema and isinstance(value, str):
        if not re.search(schema["pattern"], value):
            errors.append(f"Pattern mismatch at {path or 'root'}")
    
    # Number minimum validation
    if "minimum" in schema and isinstance(value, (int, float)):
        if value < schema["minimum"]:
            errors.append(f"Value below minimum at {path or 'root'}")
    
    # Number maximum validation
    if "maximum" in schema and isinstance(value, (int, float)):
        if value > schema["maximum"]:
            errors.append(f"Value above maximum at {path or 'root'}")
    
    # Object validation
    if isinstance(value, dict) and "properties" in schema:
        # Required properties
        if "required" in schema:
            for required_prop in schema["required"]:
                if required_prop not in value:
                    prop_path = f"{path}.{required_prop}" if path else required_prop
                    errors.append(f"Missing required property at {prop_path}")
        
        # Validate properties
        for prop_name, prop_value in value.items():
            if prop_name in schema["properties"]:
                prop_path = f"{path}.{prop_name}" if path else prop_name
                errors.extend(validate_value(prop_value, schema["properties"][prop_name], prop_path))
    
    return errors

def main():
    input_text = sys.stdin.read().strip()
    parts = input_text.split('\n\n')
    
    schema_text = parts[0]
    document_text = parts[1]
    
    try:
        schema = json.loads(schema_text)
        document = json.loads(document_text)
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        return
    
    errors = validate_value(document, schema)
    
    if not errors:
        print("Valid")
    else:
        for error in errors:
            print(error)

if __name__ == "__main__":
    main()