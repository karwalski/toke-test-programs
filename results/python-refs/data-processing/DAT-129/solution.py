import sys
import json
import csv
import io

def detect_and_parse():
    # Read all input from stdin
    input_data = sys.stdin.read().strip()
    
    # Try JSON first
    try:
        parsed = json.loads(input_data)
        print("Detected: JSON")
        print(json.dumps(parsed, separators=(',', ':')))
        return
    except json.JSONDecodeError:
        pass
    
    # Try YAML (basic detection - starts with --- or has key: value patterns)
    if (input_data.startswith('---') or 
        (':' in input_data and not ',' in input_data.split('\n')[0])):
        try:
            # Basic YAML parsing for simple cases
            result = {}
            for line in input_data.split('\n'):
                line = line.strip()
                if line and ':' in line and not line.startswith('---'):
                    key, value = line.split(':', 1)
                    result[key.strip()] = value.strip()
            if result:
                print("Detected: YAML")
                print(json.dumps(result, separators=(',', ':')))
                return
        except:
            pass
    
    # Try TOML (basic detection - has = assignments)
    if '=' in input_data and not ',' in input_data.split('\n')[0]:
        try:
            result = {}
            for line in input_data.split('\n'):
                line = line.strip()
                if line and '=' in line:
                    key, value = line.split('=', 1)
                    result[key.strip()] = value.strip().strip('"\'')
            if result:
                print("Detected: TOML")
                print(json.dumps(result, separators=(',', ':')))
                return
        except:
            pass
    
    # Try CSV
    try:
        lines = input_data.split('\n')
        if len(lines) >= 2 and ',' in lines[0]:
            csv_reader = csv.DictReader(io.StringIO(input_data))
            result = list(csv_reader)
            print("Detected: CSV")
            print(json.dumps(result, separators=(',', ':')))
            return
    except:
        pass
    
    # Default fallback
    print("Detected: Unknown")
    print(json.dumps(input_data, separators=(',', ':')))

if __name__ == "__main__":
    detect_and_parse()