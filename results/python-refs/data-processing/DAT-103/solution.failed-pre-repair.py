import sys
import json

def parse_ini_to_json():
    content = sys.stdin.read().strip()
    lines = content.split('\n')
    
    result = {}
    current_section = None
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
            
        # Check for section header
        if line.startswith('[') and line.endswith(']'):
            current_section = line[1:-1]
            result[current_section] = {}
        # Check for key=value pair
        elif '=' in line and current_section is not None:
            key, value = line.split('=', 1)
            result[current_section][key] = value
    
    # Output JSON with no spaces after separators to match expected format
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    parse_ini_to_json()