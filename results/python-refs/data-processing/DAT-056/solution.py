import json
import sys

def parse_jsonpath(path):
    """Parse a simple JSONPath expression into components"""
    # Remove leading $
    if path.startswith('$.'):
        path = path[2:]
    elif path.startswith('$'):
        path = path[1:]
    
    parts = []
    current = ""
    i = 0
    
    while i < len(path):
        if path[i] == '.':
            if current:
                parts.append(current)
                current = ""
        elif path[i] == '[':
            if current:
                parts.append(current)
                current = ""
            # Find the matching ]
            j = i + 1
            while j < len(path) and path[j] != ']':
                j += 1
            bracket_content = path[i+1:j]
            parts.append('[' + bracket_content + ']')
            i = j
        else:
            current += path[i]
        i += 1
    
    if current:
        parts.append(current)
    
    return parts

def extract_values(data, parts):
    """Extract values from JSON data using parsed JSONPath parts"""
    if not parts:
        return [data]
    
    current_part = parts[0]
    remaining_parts = parts[1:]
    
    if current_part == '*':
        results = []
        if isinstance(data, list):
            for item in data:
                results.extend(extract_values(item, remaining_parts))
        elif isinstance(data, dict):
            for value in data.values():
                results.extend(extract_values(value, remaining_parts))
        return results
    
    elif current_part.startswith('[') and current_part.endswith(']'):
        bracket_content = current_part[1:-1]
        if bracket_content == '*':
            results = []
            if isinstance(data, list):
                for item in data:
                    results.extend(extract_values(item, remaining_parts))
            elif isinstance(data, dict):
                for value in data.values():
                    results.extend(extract_values(value, remaining_parts))
            return results
        else:
            # Numeric index
            try:
                index = int(bracket_content)
                if isinstance(data, list) and 0 <= index < len(data):
                    return extract_values(data[index], remaining_parts)
            except ValueError:
                pass
            return []
    
    else:
        # Regular property access
        if isinstance(data, dict) and current_part in data:
            return extract_values(data[current_part], remaining_parts)
        return []

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

jsonpath_expr = lines[0]
json_str = lines[1]

# Parse JSON
try:
    data = json.loads(json_str)
except json.JSONDecodeError:
    sys.exit(1)

# Parse JSONPath and extract values
parts = parse_jsonpath(jsonpath_expr)
results = extract_values(data, parts)

# Output results
for result in results:
    print(json.dumps(result))