import json
import sys

def get_json_type(value):
    if isinstance(value, str):
        return "string"
    elif isinstance(value, int) and not isinstance(value, bool):
        return "int"
    elif isinstance(value, bool):
        return "bool"
    elif isinstance(value, list):
        return "array"
    elif isinstance(value, dict):
        return "object"
    else:
        return "unknown"

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    if not lines:
        return
    
    json_file_path = lines[0]
    
    # Read and parse the JSON file
    try:
        with open(json_file_path, 'r') as f:
            config = json.load(f)
    except:
        # If file doesn't exist or can't be parsed, treat as empty config
        config = {}
    
    # Process each key requirement
    for i in range(1, len(lines)):
        if not lines[i]:
            continue
        
        parts = lines[i].split()
        if len(parts) != 2:
            continue
        
        key, expected_type = parts
        
        if key not in config:
            print(f"MISSING {key}")
        else:
            actual_type = get_json_type(config[key])
            if actual_type == expected_type:
                print(f"OK {key}")
            else:
                print(f"WRONG_TYPE {key} (expected {expected_type} got {actual_type})")

if __name__ == "__main__":
    main()