import sys
import json

def extract_table():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    if len(lines) < 2:
        return {"headers": [], "rows": []}
    
    # Find the header line and separator line
    header_line = None
    separator_line = None
    data_start = 0
    
    for i, line in enumerate(lines):
        if '|' in line and (i == 0 or not all(c in '-|' for c in line.strip())):
            header_line = line
            if i + 1 < len(lines) and all(c in '-|' for c in lines[i + 1].strip()):
                separator_line = lines[i + 1]
                data_start = i + 2
                break
        elif '|' in line:
            header_line = line
            data_start = i + 1
            break
    
    if header_line is None:
        return {"headers": [], "rows": []}
    
    # Extract headers
    headers = [cell.strip() for cell in header_line.split('|')]
    
    # Extract data rows
    rows = []
    for i in range(data_start, len(lines)):
        line = lines[i]
        if '|' in line:
            row = [cell.strip() for cell in line.split('|')]
            if len(row) == len(headers):
                rows.append(row)
    
    return {"headers": headers, "rows": rows}

result = extract_table()
print(json.dumps(result, separators=(',', ':')))