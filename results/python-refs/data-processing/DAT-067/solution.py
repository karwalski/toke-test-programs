import csv
import sys

# Read CSV from stdin
reader = csv.reader(sys.stdin)
rows = list(reader)

# Transpose the matrix
transposed = list(zip(*rows))

# Write transposed CSV to stdout
writer = csv.writer(sys.stdout)
for row in transposed:
    writer.writerow(row)