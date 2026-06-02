import sys
import csv
from io import StringIO

# Read all input
input_lines = sys.stdin.read().strip().split('\n')

# First line is the split column name
split_column = input_lines[0]

# Rest is CSV data
csv_data = '\n'.join(input_lines[1:])

# Parse CSV
csv_reader = csv.DictReader(StringIO(csv_data))
rows = list(csv_reader)

# Get unique values in the split column
unique_values = []
seen = set()
for row in rows:
    value = row[split_column]
    if value not in seen:
        unique_values.append(value)
        seen.add(value)

# Group rows by the split column value
for i, value in enumerate(unique_values):
    if i > 0:
        print()  # Add blank line between groups
    
    print(f"=== {value} ===")
    
    # Print header
    print(','.join(csv_reader.fieldnames))
    
    # Print rows for this value
    for row in rows:
        if row[split_column] == value:
            print(','.join(row[field] for field in csv_reader.fieldnames))