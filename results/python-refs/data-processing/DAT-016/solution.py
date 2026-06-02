import sys
import csv
from io import StringIO

# Read all input
input_data = sys.stdin.read().strip()

# Split input into CSV data and columns to normalize
lines = input_data.split('\n')

# Find the blank line that separates CSV from columns
blank_line_idx = -1
for i, line in enumerate(lines):
    if line.strip() == '':
        blank_line_idx = i
        break

# Extract CSV data and columns to normalize
csv_data = '\n'.join(lines[:blank_line_idx])
columns_to_normalize = [line.strip() for line in lines[blank_line_idx+1:] if line.strip()]

# Parse CSV data
csv_reader = csv.DictReader(StringIO(csv_data))
rows = list(csv_reader)

# For each column to normalize, find min and max values
for col in columns_to_normalize:
    values = []
    for row in rows:
        if col in row and row[col].strip():
            try:
                values.append(float(row[col]))
            except ValueError:
                continue
    
    if values:
        min_val = min(values)
        max_val = max(values)
        
        # Normalize values
        for row in rows:
            if col in row and row[col].strip():
                try:
                    original_val = float(row[col])
                    if max_val == min_val:
                        normalized_val = 0.0
                    else:
                        normalized_val = (original_val - min_val) / (max_val - min_val)
                    row[col] = f"{normalized_val:.4f}"
                except ValueError:
                    continue

# Output the normalized CSV
if rows:
    fieldnames = csv_reader.fieldnames
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
    print(output.getvalue().strip())