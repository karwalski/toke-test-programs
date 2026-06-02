import csv
import sys
import shlex
from io import StringIO

input_lines = sys.stdin.read().split('\n')

# Parse first line - use shlex to handle quoted separator
params = shlex.split(input_lines[0])
source_columns = params[:-2]
new_column_name = params[-2]
separator = params[-1]

csv_data = '\n'.join(input_lines[1:])
csv_input = StringIO(csv_data)

reader = csv.DictReader(csv_input)
rows = list(reader)
original_columns = reader.fieldnames

new_columns = []
inserted = False
for col in original_columns:
    if col in source_columns:
        if not inserted:
            new_columns.append(new_column_name)
            inserted = True
    else:
        new_columns.append(col)
if not inserted:
    new_columns.append(new_column_name)

output = StringIO()
writer = csv.DictWriter(output, fieldnames=new_columns)
writer.writeheader()

for row in rows:
    new_row = {}
    for col in original_columns:
        if col not in source_columns:
            new_row[col] = row[col]
    combined_values = [row[col] for col in source_columns]
    new_row[new_column_name] = separator.join(combined_values)
    writer.writerow(new_row)

sys.stdout.write(output.getvalue().replace('\r\n', '\n').strip())