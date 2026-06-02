import json
import sys

def validate_openapi_spec(spec):
    errors = []
    
    # Check if spec is a dictionary
    if not isinstance(spec, dict):
        errors.append("ERROR: root - OpenAPI spec must be an object")
        return errors
    
    # Check required top-level fields
    if "openapi" not in spec:
        errors.append("ERROR: root - Missing required field 'openapi'")
    elif not isinstance(spec["openapi"], str):
        errors.append("ERROR: openapi - Must be a string")
    elif not spec["openapi"].startswith("3.0"):
        errors.append("ERROR: openapi - Must be OpenAPI 3.0.x")
    
    if "info" not in spec:
        errors.append("ERROR: root - Missing required field 'info'")
    else:
        # Validate info object
        info = spec["info"]
        if not isinstance(info, dict):
            errors.append("ERROR: info - Must be an object")
        else:
            if "title" not in info:
                errors.append("ERROR: info - Missing required field 'title'")
            elif not isinstance(info["title"], str):
                errors.append("ERROR: info.title - Must be a string")
            
            if "version" not in info:
                errors.append("ERROR: info - Missing required field 'version'")
            elif not isinstance(info["version"], str):
                errors.append("ERROR: info.version - Must be a string")
    
    if "paths" not in spec:
        errors.append("ERROR: root - Missing required field 'paths'")
    elif not isinstance(spec["paths"], dict):
        errors.append("ERROR: paths - Must be an object")
    
    return errors

def main():
    try:
        # Read JSON from stdin
        input_data = sys.stdin.read().strip()
        spec = json.loads(input_data)
        
        # Validate the spec
        errors = validate_openapi_spec(spec)
        
        if errors:
            for error in errors:
                print(error)
        else:
            print("VALID")
    
    except json.JSONDecodeError:
        print("ERROR: root - Invalid JSON format")
    except Exception as e:
        print(f"ERROR: root - {str(e)}")

if __name__ == "__main__":
    main()