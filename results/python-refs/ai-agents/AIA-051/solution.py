import sys
import json
import re

def extract_key_value_pairs():
    data = {}
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
            
        # Look for key-value pattern: "Key: Value"
        match = re.match(r'^([^:]+):\s*(.*)$', line)
        if match:
            key = match.group(1).strip()
            value = match.group(2).strip()
            data[key] = value
    
    # Output JSON without spaces after separators to match expected format
    print(json.dumps(data, separators=(',', ':')))

if __name__ == "__main__":
    extract_key_value_pairs()