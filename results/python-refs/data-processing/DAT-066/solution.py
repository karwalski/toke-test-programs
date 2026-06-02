import csv
import sys
from datetime import datetime

def detect_type(values):
    # Remove empty values for type detection
    non_empty_values = [v for v in values if v.strip()]
    
    if not non_empty_values:
        return "string"
    
    # Check for boolean
    bool_values = {"true", "false", "1", "0", "yes", "no"}
    if all(v.lower() in bool_values for v in non_empty_values):
        return "boolean"
    
    # Check for integer
    try:
        for v in non_empty_values:
            int(v)
        return "integer"
    except ValueError:
        pass
    
    # Check for float
    try:
        for v in non_empty_values:
            float(v)
        return "float"
    except ValueError:
        pass
    
    # Check for date
    date_formats = [
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%d/%m/%Y",
        "%Y/%m/%d",
        "%m-%d-%Y",
        "%d-%m-%Y"
    ]
    
    is_date = True
    for v in non_empty_values:
        date_found = False
        for fmt in date_formats:
            try:
                datetime.strptime(v, fmt)
                date_found = True
                break
            except ValueError:
                continue
        if not date_found:
            is_date = False
            break
    
    if is_date:
        return "date"
    
    return "string"

# Read CSV from stdin
reader = csv.reader(sys.stdin)
headers = next(reader)
rows = list(reader)

# Collect values for each column
columns = {header: [] for header in headers}
for row in rows:
    for i, value in enumerate(row):
        if i < len(headers):
            columns[headers[i]].append(value)

# Detect and output types
for header in headers:
    detected_type = detect_type(columns[header])
    print(f"{header}\t{detected_type}")