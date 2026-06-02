import sys
import json

def parse_ini_to_json():
    content = sys.stdin.read().strip()
    lines = content.split('\n')
    
    result = {}
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith(';') or line.startswith('#'):
            continue
        if line.startswith('[') and line.endswith(']'):
            current_section = line[1:-1]
            if current_section not in result:
                result[current_section] = {}
        elif '=' in line:
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            if current_section is None:
                if '__global__' not in result:
                    result['__global__'] = {}
                result['__global__'][key] = value
            else:
                result[current_section][key] = value
    
    # Sort keys within each section
    sorted_result = {}
    for section in sorted(result.keys()):
        sorted_result[section] = {k: result[section][k] for k in sorted(result[section].keys())}
    
    print(json.dumps(sorted_result, separators=(',', ':')))

if __name__ == "__main__":
    parse_ini_to_json()