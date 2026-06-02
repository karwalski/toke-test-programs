import csv
import json
import sys
from collections import Counter

def infer_type(values):
    # Remove empty values for type inference
    non_empty_values = [v for v in values if v.strip()]
    
    if not non_empty_values:
        return "string"
    
    # Check if all values are integers
    try:
        for v in non_empty_values:
            int(v)
        return "integer"
    except ValueError:
        pass
    
    # Check if all values are floats
    try:
        for v in non_empty_values:
            float(v)
        return "float"
    except ValueError:
        pass
    
    return "string"

def convert_value(value, data_type):
    if data_type == "integer":
        return int(value)
    elif data_type == "float":
        return float(value)
    else:
        return value

def profile_column(values):
    total_count = len(values)
    non_empty_count = sum(1 for v in values if v.strip())
    
    completeness = non_empty_count / total_count if total_count > 0 else 0.0
    
    # Infer type based on non-empty values
    data_type = infer_type(values)
    
    # Convert values to appropriate type for analysis
    converted_values = []
    for v in values:
        if v.strip():
            converted_values.append(convert_value(v, data_type))
    
    # Calculate cardinality (unique values)
    unique_values = set(converted_values)
    cardinality = len(unique_values)
    
    # Get top values (most frequent)
    value_counts = Counter(converted_values)
    top_values = [value for value, count in value_counts.most_common()]
    
    return {
        "type": data_type,
        "completeness": completeness,
        "cardinality": cardinality,
        "top_values": top_values
    }

# Read CSV from stdin
reader = csv.reader(sys.stdin)
headers = next(reader)
rows = list(reader)

# Transpose data to get columns
columns = {}
for i, header in enumerate(headers):
    column_values = [row[i] if i < len(row) else "" for row in rows]
    columns[header] = column_values

# Profile each column
profile = {}
for header, values in columns.items():
    profile[header] = profile_column(values)

# Output JSON
print(json.dumps(profile, separators=(',', ':')))