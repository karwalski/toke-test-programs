import csv
import sys
from io import StringIO

# Read all input
input_data = sys.stdin.read().strip()

# Split by double newlines to separate the datasets and join command
parts = input_data.split('\n\n')
dataset_a_text = parts[0]
dataset_b_text = parts[1]
join_command = parts[2]

# Parse the join command to get column names
join_parts = join_command.replace('join ', '').split('=')
col_a = join_parts[0].strip()
col_b = join_parts[1].strip()

# Parse dataset A
reader_a = csv.DictReader(StringIO(dataset_a_text))
data_a = list(reader_a)
headers_a = reader_a.fieldnames

# Parse dataset B
reader_b = csv.DictReader(StringIO(dataset_b_text))
data_b = list(reader_b)
headers_b = reader_b.fieldnames

# Create index for dataset B for faster lookup
b_index = {}
for row in data_b:
    key = row[col_b]
    b_index[key] = row

# Perform inner join
result_rows = []
for row_a in data_a:
    key = row_a[col_a]
    if key in b_index:
        # Create joined row
        joined_row = row_a.copy()
        row_b = b_index[key]
        for field in headers_b:
            if field != col_b:  # Avoid duplicate key column
                joined_row[field] = row_b[field]
        result_rows.append(joined_row)

# Create output headers (A's headers + B's headers except the duplicate key)
output_headers = headers_a[:]
for header in headers_b:
    if header != col_b:
        output_headers.append(header)

# Write output
writer = csv.DictWriter(sys.stdout, fieldnames=output_headers, lineterminator='\n')
writer.writeheader()
writer.writerows(result_rows)