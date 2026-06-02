import sys
import csv
import io
import math

# Read all input
input_data = sys.stdin.read().strip()

# Split input into CSV part and column names part
parts = input_data.split('\n\n')
csv_data = parts[0]
columns_to_normalize = parts[1].split()

# Parse CSV data
csv_reader = csv.DictReader(io.StringIO(csv_data))
rows = list(csv_reader)
fieldnames = csv_reader.fieldnames

# For each column to normalize, calculate z-scores
for col_name in columns_to_normalize:
    if col_name in fieldnames:
        # Extract numeric values
        values = [float(row[col_name]) for row in rows]
        
        # Calculate mean and standard deviation
        n = len(values)
        mean = sum(values) / n
        variance = sum((x - mean) ** 2 for x in values) / n
        std_dev = math.sqrt(variance)
        
        # Calculate z-scores and update rows
        for i, row in enumerate(rows):
            if std_dev == 0:
                z_score = 0.0
            else:
                z_score = (values[i] - mean) / std_dev
            row[col_name] = f"{z_score:.4f}"

# Output the normalized CSV
output = io.StringIO()
csv_writer = csv.DictWriter(output, fieldnames=fieldnames)
csv_writer.writeheader()
csv_writer.writerows(rows)

print(output.getvalue().strip())