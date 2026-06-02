import sys
import csv
from io import StringIO

# Read input
lines = sys.stdin.read().strip().split('\n')
mode_line = lines[0].split()
mode = mode_line[0]
bin_count = int(mode_line[1])
column_name = lines[1]

# Parse CSV data
csv_data = '\n'.join(lines[2:])
csv_reader = csv.DictReader(StringIO(csv_data))
records = list(csv_reader)

# Extract numeric values from the specified column
values = [float(record[column_name]) for record in records]

# Create bins based on mode
if mode == 'quantile':
    # Sort values to find quantile boundaries
    sorted_values = sorted(values)
    n = len(sorted_values)
    
    # Calculate quantile boundaries
    boundaries = []
    for i in range(1, bin_count):
        # Use simple quantile calculation
        pos = i * n / bin_count
        if pos == int(pos):
            # Exact position - use that value
            boundaries.append(sorted_values[int(pos) - 1])
        else:
            # Between positions - use the ceiling position
            boundaries.append(sorted_values[int(pos)])
    
    # Assign bins
    for record in records:
        value = float(record[column_name])
        bin_num = 1
        for boundary in boundaries:
            if value > boundary:
                bin_num += 1
            else:
                break
        record[f'{column_name}_bin'] = f'Q{bin_num}'

elif mode == 'equalwidth':
    # Find min and max values
    min_val = min(values)
    max_val = max(values)
    
    # Calculate bin width
    width = (max_val - min_val) / bin_count
    
    # Assign bins
    for record in records:
        value = float(record[column_name])
        if value == max_val:
            bin_num = bin_count
        else:
            bin_num = min(int((value - min_val) / width) + 1, bin_count)
        record[f'{column_name}_bin'] = f'B{bin_num}'

# Output CSV
fieldnames = list(records[0].keys())
writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames, lineterminator='\n')
writer.writeheader()
writer.writerows(records)