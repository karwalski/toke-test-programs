import sys
import csv
from io import StringIO

# Read all input from stdin
input_data = sys.stdin.read().strip()

# Split into lines
lines = input_data.split('\n')

# Create CSV writer to stdout
csv_writer = csv.writer(sys.stdout, quoting=csv.QUOTE_MINIMAL)

# Process each line
for line in lines:
    # Split by tabs to get fields
    fields = line.split('\t')
    # Write as CSV row
    csv_writer.writerow(fields)