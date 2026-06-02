import sys

# Read input
lines = [line.strip() for line in sys.stdin.readlines()]

# Parse nodes
nodes = lines[0].split()
n = len(nodes)

# Create node to index mapping
node_to_idx = {node: i for i, node in enumerate(nodes)}

# Initialize adjacency matrix
matrix = [[0 for _ in range(n)] for _ in range(n)]

# Parse edges and fill matrix
for i in range(1, len(lines)):
    if lines[i]:  # Skip empty lines
        parts = lines[i].split()
        from_node = parts[0]
        to_node = parts[1]
        weight = int(parts[2])
        
        from_idx = node_to_idx[from_node]
        to_idx = node_to_idx[to_node]
        matrix[from_idx][to_idx] = weight

# Output as CSV
# Header row
print(',' + ','.join(nodes))

# Matrix rows
for i, node in enumerate(nodes):
    row = [node] + [str(matrix[i][j]) for j in range(n)]
    print(','.join(row))