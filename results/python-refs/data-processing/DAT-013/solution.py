import sys
import json
from datetime import datetime

def parse_type_specs():
    type_specs = {}
    for line in sys.stdin:
        line = line.strip()
        if not line:
            break
        field, type_name = line.split(':')
        type_specs[field] = type_name
    return type_specs

def cast_value(value, type_name):
    if type_name == 'int':
        return int(value)
    elif type_name == 'float':
        return float(value)
    elif type_name == 'bool':
        if isinstance(value, str):
            return value.lower() in ('true', '1', 'yes')
        return bool(value)
    elif type_name == 'string':
        return str(value)
    elif type_name == 'date':
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace('Z', '+00:00')).isoformat()
        return value
    return value

def main():
    type_specs = parse_type_specs()
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        obj = json.loads(line)
        
        for field, type_name in type_specs.items():
            if field in obj:
                obj[field] = cast_value(obj[field], type_name)
        
        print(json.dumps(obj, separators=(',', ':')))

if __name__ == "__main__":
    main()