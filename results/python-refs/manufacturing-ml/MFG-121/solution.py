import csv
import json
import sys
import math

def euclidean_distance(point1, point2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(point1, point2)))

# Read CSV from stdin
reader = csv.reader(sys.stdin)
header = next(reader)
data = []

for row in reader:
    data.append([float(val) for val in row])

# Calculate pairwise distance matrix
n = len(data)
distance_matrix = []

for i in range(n):
    row = []
    for j in range(n):
        if i == j:
            distance = 0.0
        else:
            distance = euclidean_distance(data[i], data[j])
            distance = round(distance, 2)
        row.append(distance)
    distance_matrix.append(row)

# Output as JSON
result = {"distance_matrix": distance_matrix}
print(json.dumps(result, separators=(',', ':')))