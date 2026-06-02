import sys
import csv
from io import StringIO

# Read all input
input_data = sys.stdin.read().strip()

# Split input into CSV data and key columns
parts = input_data.split('\n\n')
csv_data = parts[0]
key_columns = parts[1].split()

# Parse CSV data
csv_reader = csv.DictReader(StringIO(csv_data))
rows = list(csv_reader)

# Track seen key combinations
seen_keys = set()
unique_rows = []

for row in rows:
    # Create key tuple from specified columns
    key = tuple(row[col] for col in key_columns)
    
    if key not in seen_keys:
        seen_keys.add(key)
        unique_rows.append(row)

# Output CSV
if unique_rows:
    fieldnames = unique_rows[0].keys()
    csv_writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames, lineterminator='\n')
    csv_writer.writeheader()
    csv_writer.writerows(unique_rows)