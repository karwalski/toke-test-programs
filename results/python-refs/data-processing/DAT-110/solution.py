import json
import csv
import sys
from io import StringIO

def flatten_object(obj, parent_key='', sep='.'):
    """
    Flatten a nested dictionary into a flat dictionary with dot notation keys.
    """
    items = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(flatten_object(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                # Convert list to JSON string representation
                items.append((new_key, json.dumps(v)))
            else:
                items.append((new_key, v))
    else:
        return {parent_key: obj}
    return dict(items)

def main():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    
    # Parse JSON
    data = json.loads(input_data)
    
    # Flatten each object
    flattened_objects = []
    all_keys = set()
    
    for obj in data:
        flattened = flatten_object(obj)
        flattened_objects.append(flattened)
        all_keys.update(flattened.keys())
    
    # Sort keys to ensure consistent column order
    sorted_keys = sorted(all_keys)
    
    # Create CSV output
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=sorted_keys, quoting=csv.QUOTE_MINIMAL)
    
    # Write header
    writer.writeheader()
    
    # Write data rows
    for obj in flattened_objects:
        # Fill missing keys with empty strings
        row = {key: obj.get(key, '') for key in sorted_keys}
        writer.writerow(row)
    
    # Get the CSV content and print it
    csv_content = output.getvalue().strip()
    print(csv_content)

if __name__ == "__main__":
    main()