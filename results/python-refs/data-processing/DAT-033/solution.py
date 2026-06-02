import sys
import csv
from io import StringIO

# Read all input
input_text = sys.stdin.read().strip()

# Split by double newlines to get the three parts
parts = input_text.split('\n\n')
dataset_a_text = parts[0]
dataset_b_text = parts[1]
join_command = parts[2]

# Parse the join command to get column names
join_parts = join_command.split('=')
left_col = join_parts[0].replace('join ', '').strip()
right_col = join_parts[1].strip()

# Parse dataset A
dataset_a_reader = csv.reader(StringIO(dataset_a_text))
a_rows = list(dataset_a_reader)
a_headers = a_rows[0]
a_data = a_rows[1:]

# Parse dataset B
dataset_b_reader = csv.reader(StringIO(dataset_b_text))
b_rows = list(dataset_b_reader)
b_headers = b_rows[0]
b_data = b_rows[1:]

# Find column indices
left_col_idx = a_headers.index(left_col)
right_col_idx = b_headers.index(right_col)

# Create lookup dictionary for dataset B
b_lookup = {}
for row in b_data:
    key = row[right_col_idx]
    b_lookup[key] = row

# Create output headers (A headers + B headers except the join column)
output_headers = a_headers[:]
for header in b_headers:
    if header != right_col:
        output_headers.append(header)

# Perform left join
result_rows = []
for a_row in a_data:
    join_key = a_row[left_col_idx]
    result_row = a_row[:]
    
    if join_key in b_lookup:
        b_row = b_lookup[join_key]
        # Add all columns from B except the join column
        for i, header in enumerate(b_headers):
            if header != right_col:
                result_row.append(b_row[i])
    else:
        # Add empty strings for unmatched rows
        for header in b_headers:
            if header != right_col:
                result_row.append('')
    
    result_rows.append(result_row)

# Output the result
output = StringIO()
writer = csv.writer(output)
writer.writerow(output_headers)
writer.writerows(result_rows)
print(output.getvalue().strip())