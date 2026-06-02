import sys
import csv
import re
import shlex

first_line = sys.stdin.readline().rstrip('\n')
parts = shlex.split(first_line)
source_column = parts[0]
new_columns = parts[1:-1]
delimiter = parts[-1]

input_lines = []
for line in sys.stdin:
    input_lines.append(line.rstrip('\n'))

reader = csv.reader(input_lines)
rows = list(reader)

if not rows:
    sys.exit()

header = rows[0]
data_rows = rows[1:]

try:
    source_index = header.index(source_column)
except ValueError:
    sys.exit()

new_header = header[:source_index] + new_columns + header[source_index + 1:]

n = len(new_columns)
new_data_rows = []
for row in data_rows:
    if source_index < len(row):
        source_value = row[source_index]
        
        if delimiter.startswith('/') and delimiter.endswith('/') and len(delimiter) > 2:
            pattern = delimiter[1:-1]
            split_values = re.split(pattern, source_value, maxsplit=n-1)
        else:
            split_values = source_value.split(delimiter, n-1)
        
        while len(split_values) < n:
            split_values.append('')
        
        new_row = row[:source_index] + split_values + row[source_index + 1:]
        new_data_rows.append(new_row)
    else:
        empty_values = [''] * n
        new_row = row[:source_index] + empty_values + row[source_index + 1:]
        new_data_rows.append(new_row)

writer = csv.writer(sys.stdout, lineterminator='\n')
writer.writerow(new_header)
for row in new_data_rows:
    writer.writerow(row)