import json
import sys

def jsonpath_extract(jsonpath, data):
    """Simple JSONPath implementation for basic expressions"""
    
    # Remove leading $. if present
    if jsonpath.startswith('$.'):
        jsonpath = jsonpath[2:]
    elif jsonpath.startswith('$'):
        jsonpath = jsonpath[1:]
    
    # If empty path after removing $, return the whole data
    if not jsonpath:
        return [data]
    
    # Split path into parts
    parts = []
    current = ""
    i = 0
    while i < len(jsonpath):
        if jsonpath[i] == '.':
            if current:
                parts.append(current)
                current = ""
        elif jsonpath[i] == '[':
            if current:
                parts.append(current)
                current = ""
            # Find matching ]
            j = i + 1
            while j < len(jsonpath) and jsonpath[j] != ']':
                j += 1
            if j < len(jsonpath):
                bracket_content = jsonpath[i+1:j]
                parts.append(f"[{bracket_content}]")
                i = j
            else:
                current += jsonpath[i]
        else:
            current += jsonpath[i]
        i += 1
    
    if current:
        parts.append(current)
    
    # Navigate through the data
    results = [data]
    
    for part in parts:
        new_results = []
        for item in results:
            if part.startswith('[') and part.endswith(']'):
                # Array index or wildcard
                bracket_content = part[1:-1]
                if bracket_content == '*':
                    # Wildcard - get all elements
                    if isinstance(item, list):
                        new_results.extend(item)
                    elif isinstance(item, dict):
                        new_results.extend(item.values())
                else:
                    try:
                        # Try as array index
                        index = int(bracket_content)
                        if isinstance(item, list) and 0 <= index < len(item):
                            new_results.append(item[index])
                    except ValueError:
                        # Try as dict key
                        if isinstance(item, dict) and bracket_content.strip('\'"') in item:
                            key = bracket_content.strip('\'"')
                            new_results.append(item[key])
            else:
                # Regular property access
                if isinstance(item, dict) and part in item:
                    new_results.append(item[part])
        
        results = new_results
    
    return results

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

if not lines:
    sys.exit(0)

jsonpath_expr = lines[0]
json_text = '\n'.join(lines[1:])

try:
    data = json.loads(json_text)
    results = jsonpath_extract(jsonpath_expr, data)
    
    for result in results:
        if isinstance(result, str):
            print(result)
        else:
            print(json.dumps(result, separators=(',', ':')))
            
except json.JSONDecodeError:
    pass
except Exception:
    pass