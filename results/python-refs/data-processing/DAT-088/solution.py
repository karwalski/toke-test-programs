import csv
import sys

# Read CSV from stdin
reader = csv.reader(sys.stdin)
rows = list(reader)

# Extract header (node names)
header = rows[0][1:]  # Skip first empty cell
nodes = header

# Process adjacency matrix
edges = []
for i, row in enumerate(rows[1:]):
    from_node = row[0]
    for j, weight in enumerate(row[1:]):
        weight = weight.strip()
        if weight and weight != '0':
            to_node = nodes[j]
            edges.append((from_node, to_node, weight))

# Sort by from node, then by to node
edges.sort(key=lambda x: (x[0], x[1]))

# Output edge list
for from_node, to_node, weight in edges:
    print(f"{from_node} {to_node} {weight}")