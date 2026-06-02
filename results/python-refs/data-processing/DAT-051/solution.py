import sys
import csv
from io import StringIO

# Read all input
input_lines = sys.stdin.read().strip().split('\n')

# First line contains the columns to keep
columns_to_keep = input_lines[0].split()

# Remaining lines are the CSV data
csv_data = '\n'.join(input_lines[1:])

# Parse the CSV
csv_reader = csv.reader(StringIO(csv_data))
headers = next(csv_reader)

# Find indices of columns to keep
column_indices = []
for col in columns_to_keep:
    if col in headers:
        column_indices.append(headers.index(col))

# Output the selected columns header
print(','.join(columns_to_keep))

# Output the data rows with selected columns
for row in csv_reader:
    selected_values = []
    for idx in column_indices:
        selected_values.append(row[idx])
    print(','.join(selected_values))