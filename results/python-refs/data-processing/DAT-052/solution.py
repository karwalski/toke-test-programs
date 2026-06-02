import sys
import csv
import random

# Read the first line to get sampling parameters
first_line = input().strip()
parts = first_line.split()
mode = parts[0]
n = int(parts[1])
seed = None
if mode == "random" and len(parts) > 2:
    seed = int(parts[2])
    random.seed(seed)

# Read all remaining lines as CSV data
csv_lines = []
for line in sys.stdin:
    csv_lines.append(line.rstrip('\n'))

if not csv_lines:
    sys.exit()

# Parse CSV
reader = csv.reader(csv_lines)
rows = list(reader)

if not rows:
    sys.exit()

header = rows[0]
data_rows = rows[1:]

# Sample based on mode
if mode == "head":
    sampled_rows = data_rows[:n]
elif mode == "tail":
    sampled_rows = data_rows[-n:]
elif mode == "random":
    sampled_rows = random.sample(data_rows, min(n, len(data_rows)))

# Output CSV
writer = csv.writer(sys.stdout, lineterminator='\n')
writer.writerow(header)
for row in sampled_rows:
    writer.writerow(row)