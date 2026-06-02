import sys
import csv
from io import StringIO

# Read all input
lines = sys.stdin.read().strip().split('\n')

# Parse first line
first_line = lines[0].split()
n = int(first_line[0])
sort_column = first_line[1]
order = first_line[2]

# Parse CSV data
csv_data = '\n'.join(lines[1:])
csv_reader = csv.DictReader(StringIO(csv_data))

# Read all rows
rows = list(csv_reader)

# Determine if numeric sorting is needed
try:
    float(rows[0][sort_column])
    is_numeric = True
except (ValueError, KeyError):
    is_numeric = False

# Sort rows
if is_numeric:
    rows.sort(key=lambda x: float(x[sort_column]), reverse=(order == 'desc'))
else:
    rows.sort(key=lambda x: x[sort_column], reverse=(order == 'desc'))

# Get top N rows
top_rows = rows[:n]

# Output header
print(','.join(csv_reader.fieldnames))

# Output top N rows
for row in top_rows:
    print(','.join(row[field] for field in csv_reader.fieldnames))