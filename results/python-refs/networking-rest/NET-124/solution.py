import sys
import json
import urllib.request
import urllib.error

def validate_json(data, schema):
    """Simple JSON schema validation for required fields only"""
    if not isinstance(data, dict):
        return False, "Response is not a JSON object"
    
    if "required" in schema:
        for field in schema["required"]:
            if field not in data:
                return False, f"Missing required field: {field}"
    
    return True, ""

def main():
    # Read input
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    if not lines:
        print("FAIL: No input provided")
        return
    
    url = lines[0]
    schema_lines = lines[1:]
    
    if not schema_lines:
        print("FAIL: No schema provided")
        return
    
    # Parse schema
    try:
        schema_text = '\n'.join(schema_lines)
        schema = json.loads(schema_text)
    except json.JSONDecodeError as e:
        print(f"FAIL: Invalid JSON schema: {e}")
        return
    
    # Fetch URL
    try:
        with urllib.request.urlopen(url) as response:
            response_body = response.read().decode('utf-8')
    except urllib.error.URLError as e:
        print(f"FAIL: Failed to fetch URL: {e}")
        return
    except Exception as e:
        print(f"FAIL: Error fetching URL: {e}")
        return
    
    # Parse response
    try:
        response_data = json.loads(response_body)
    except json.JSONDecodeError as e:
        print(f"FAIL: Response is not valid JSON: {e}")
        return
    
    # Validate against schema
    is_valid, error_msg = validate_json(response_data, schema)
    
    if is_valid:
        print("PASS")
    else:
        print(f"FAIL: {error_msg}")

if __name__ == "__main__":
    main()