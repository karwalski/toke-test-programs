import sys
import json
import csv
from io import StringIO

# Read all input
input_data = sys.stdin.read().strip()
lines = input_data.split('\n')

# Parse split ratio from first line
split_ratio = float(lines[0])

# Parse CSV data from remaining lines
csv_data = '\n'.join(lines[1:])
csv_reader = csv.reader(StringIO(csv_data))

# Count data rows (excluding header)
rows = list(csv_reader)
total_rows = len(rows) - 1  # Subtract 1 for header

# Calculate split
train_count = int(total_rows * split_ratio)
test_count = total_rows - train_count

# Output JSON
result = {
    "train_count": train_count,
    "test_count": test_count,
    "split_ratio": split_ratio
}

print(json.dumps(result, separators=(',', ':')))