import sys
import json

def validate_config(schema, config):
    errors = []
    
    # Check required fields
    if "required" in schema:
        for field in schema["required"]:
            if field not in config:
                errors.append(f"ERROR: {field} - required field missing")
    
    # Check types
    if "types" in schema:
        for field, expected_type in schema["types"].items():
            if field in config:
                value = config[field]
                if expected_type == "string" and not isinstance(value, str):
                    errors.append(f"ERROR: {field} - expected string")
                elif expected_type == "integer" and not isinstance(value, int):
                    errors.append(f"ERROR: {field} - expected integer")
                elif expected_type == "number" and not isinstance(value, (int, float)):
                    errors.append(f"ERROR: {field} - expected number")
                elif expected_type == "boolean" and not isinstance(value, bool):
                    errors.append(f"ERROR: {field} - expected boolean")
    
    return errors

# Read input from stdin
input_text = sys.stdin.read().strip()

# Split on '---' separator
parts = input_text.split('\n---\n')
schema_text = parts[0]
config_text = parts[1]

# Parse JSON
try:
    schema = json.loads(schema_text)
    config = json.loads(config_text)
except json.JSONDecodeError as e:
    print(f"ERROR: JSON parse error - {e}")
    sys.exit(1)

# Validate
errors = validate_config(schema, config)

# Output results
if errors:
    for error in errors:
        print(error)
else:
    print("VALID")