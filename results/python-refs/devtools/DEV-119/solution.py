import json
import sys

def validate_plugin_manifest(manifest):
    errors = []
    
    # Check required fields
    required_fields = ["name", "version", "main", "api_version"]
    for field in required_fields:
        if field not in manifest:
            errors.append(f"Missing required field: {field}")
    
    # Validate field types and values
    if "name" in manifest:
        if not isinstance(manifest["name"], str) or not manifest["name"].strip():
            errors.append("Field 'name' must be a non-empty string")
    
    if "version" in manifest:
        if not isinstance(manifest["version"], str) or not manifest["version"].strip():
            errors.append("Field 'version' must be a non-empty string")
    
    if "main" in manifest:
        if not isinstance(manifest["main"], str) or not manifest["main"].strip():
            errors.append("Field 'main' must be a non-empty string")
    
    if "api_version" in manifest:
        if not isinstance(manifest["api_version"], str) or not manifest["api_version"].strip():
            errors.append("Field 'api_version' must be a non-empty string")
    
    return errors

def main():
    try:
        # Read JSON from stdin
        input_data = sys.stdin.read().strip()
        manifest = json.loads(input_data)
        
        # Validate the manifest
        errors = validate_plugin_manifest(manifest)
        
        if errors:
            for error in errors:
                print(error)
        else:
            print("VALID")
            
    except json.JSONDecodeError:
        print("Invalid JSON format")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()