import csv
import sys
from io import StringIO

# Read all input
input_lines = sys.stdin.read().strip().split('\n')

# Parse the first line to get parameters
params = input_lines[0].split()
source_columns = params[:-2]
new_column_name = params[-2]
separator = params[-1]

# Handle quoted separator (remove quotes if present)
if separator.startswith('"') and separator.endswith('"'):
    separator = separator[1:-1]

# Parse CSV data from remaining lines
csv_data = '\n'.join(input_lines[1:])
csv_input = StringIO(csv_data)

# Read CSV
reader = csv.DictReader(csv_input)
rows = list(reader)

# Get all column names and create new column order
original_columns = reader.fieldnames
new_columns = []

# Add columns that are not being combined
for col in original_columns:
    if col not in source_columns:
        new_columns.append(col)

# Add the new combined column
new_columns.append(new_column_name)

# Create output
output = StringIO()
writer = csv.DictWriter(output, fieldnames=new_columns)
writer.writeheader()

for row in rows:
    new_row = {}
    
    # Copy non-combined columns
    for col in original_columns:
        if col not in source_columns:
            new_row[col] = row[col]
    
    # Create combined column
    combined_values = [row[col] for col in source_columns]
    new_row[new_column_name] = separator.join(combined_values)
    
    writer.writerow(new_row)

# Output the result
print(output.getvalue().strip())