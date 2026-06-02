import sys
import csv
import json
import math

reader = csv.reader(sys.stdin)
headers = next(reader)
rows = []
for row in reader:
    rows.append([float(x) for x in row])

num_features = len(headers)
num_rows = len(rows)
means = []
for col in range(num_features):
    total = sum(rows[row][col] for row in range(num_rows))
    means.append(total / num_rows)

stds = []
for col in range(num_features):
    variance = sum((rows[row][col] - means[col]) ** 2 for row in range(num_rows)) / (num_rows - 1)
    stds.append(math.sqrt(variance))

standardised = []
for row in range(num_rows):
    std_row = []
    for col in range(num_features):
        std_value = (rows[row][col] - means[col]) / stds[col]
        std_row.append(round(std_value, 2))
    standardised.append(std_row)

means = [int(x) if x == int(x) else x for x in means]
stds = [int(x) if x == int(x) else x for x in stds]

result = {
    "standardised": standardised,
    "means": means,
    "stds": stds
}

print(json.dumps(result, separators=(',', ':')))