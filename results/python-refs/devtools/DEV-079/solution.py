import json
import sys

def validate_payload():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    # Parse the required fields spec
    spec = json.loads(lines[0])
    
    # Parse the JSON payload
    payload = json.loads(lines[1])
    
    errors = []
    
    # Check for missing fields and type errors
    for field, expected_type in spec.items():
        if field not in payload:
            errors.append(f"MISSING: {field}")
        else:
            value = payload[field]
            
            # Check type
            if expected_type == "string" and not isinstance(value, str):
                actual_type = type(value).__name__
                if actual_type == "int":
                    actual_type = "integer"
                elif actual_type == "float":
                    actual_type = "number"
                elif actual_type == "bool":
                    actual_type = "boolean"
                errors.append(f"TYPE ERROR: {field} (expected {expected_type} got {actual_type})")
            elif expected_type == "integer" and not isinstance(value, int):
                actual_type = type(value).__name__
                if actual_type == "str":
                    actual_type = "string"
                elif actual_type == "float":
                    actual_type = "number"
                elif actual_type == "bool":
                    actual_type = "boolean"
                errors.append(f"TYPE ERROR: {field} (expected {expected_type} got {actual_type})")
            elif expected_type == "number" and not isinstance(value, (int, float)):
                actual_type = type(value).__name__
                if actual_type == "str":
                    actual_type = "string"
                elif actual_type == "int":
                    actual_type = "integer"
                elif actual_type == "bool":
                    actual_type = "boolean"
                errors.append(f"TYPE ERROR: {field} (expected {expected_type} got {actual_type})")
            elif expected_type == "boolean" and not isinstance(value, bool):
                actual_type = type(value).__name__
                if actual_type == "str":
                    actual_type = "string"
                elif actual_type == "int":
                    actual_type = "integer"
                elif actual_type == "float":
                    actual_type = "number"
                errors.append(f"TYPE ERROR: {field} (expected {expected_type} got {actual_type})")
    
    if errors:
        for error in errors:
            print(error)
    else:
        print("VALID")

validate_payload()