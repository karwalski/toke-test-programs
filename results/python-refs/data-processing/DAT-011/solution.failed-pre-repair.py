import sys
import json

def parse_fixed_width():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    # Parse schema
    schema = []
    i = 0
    while i < len(lines) and lines[i].strip():
        parts = lines[i].split()
        name = parts[0]
        start = int(parts[1])
        width = int(parts[2])
        schema.append((name, start, width))
        i += 1
    
    # Skip blank line
    i += 1
    
    # Process data lines
    while i < len(lines):
        data_line = lines[i]
        record = {}
        
        for name, start, width in schema:
            # Extract field value, handling case where line might be shorter
            if start < len(data_line):
                end = min(start + width, len(data_line))
                value = data_line[start:end].rstrip()
            else:
                value = ""
            record[name] = value
        
        print(json.dumps(record, separators=(',', ':')))
        i += 1

parse_fixed_width()