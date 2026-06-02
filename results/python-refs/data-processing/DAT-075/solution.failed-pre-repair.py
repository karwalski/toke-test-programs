import sys
import csv
import re

# Read the first line to get parameters
first_line = input().strip()
parts = first_line.split()
source_column = parts[0]
new_columns = parts[1:-1]
delimiter = parts[-1]

# Read all remaining input
input_lines = []
for line in sys.stdin:
    input_lines.append(line.rstrip('\n'))

# Parse CSV
reader = csv.reader(input_lines)
rows = list(reader)

if not rows:
    sys.exit()

header = rows[0]
data_rows = rows[1:]

# Find the index of the source column
try:
    source_index = header.index(source_column)
except ValueError:
    sys.exit()

# Create new header
new_header = header[:source_index] + new_columns + header[source_index + 1:]

# Process data rows
new_data_rows = []
for row in data_rows:
    if source_index < len(row):
        source_value = row[source_index]
        
        # Split the value using delimiter
        if delimiter.startswith('/') and delimiter.endswith('/') and len(delimiter) > 2:
            # Regex delimiter
            pattern = delimiter[1:-1]
            split_values = re.split(pattern, source_value)
        else:
            # Regular delimiter
            split_values = source_value.split(delimiter)
        
        # Ensure we have enough values for all new columns
        while len(split_values) < len(new_columns):
            split_values.append('')
        
        # Create new row
        new_row = row[:source_index] + split_values[:len(new_columns)] + row[source_index + 1:]
        new_data_rows.append(new_row)
    else:
        # Handle case where row doesn't have enough columns
        empty_values = [''] * len(new_columns)
        new_row = row[:source_index] + empty_values + row[source_index + 1:]
        new_data_rows.append(new_row)

# Output CSV
writer = csv.writer(sys.stdout, lineterminator='\n')
writer.writerow(new_header)
for row in new_data_rows:
    writer.writerow(row)