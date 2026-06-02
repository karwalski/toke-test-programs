import sys

# Read number of vertices
V = int(input())

# Read adjacency matrix
dist = []
for i in range(V):
    row = input().split()
    processed_row = []
    for val in row:
        if val == "INF":
            processed_row.append(float('inf'))
        else:
            processed_row.append(int(val))
    dist.append(processed_row)

# Floyd-Warshall algorithm
for k in range(V):
    for i in range(V):
        for j in range(V):
            if dist[i][k] + dist[k][j] < dist[i][j]:
                dist[i][j] = dist[i][k] + dist[k][j]

# Output the result
for i in range(V):
    row_output = []
    for j in range(V):
        if dist[i][j] == float('inf'):
            row_output.append("INF")
        else:
            row_output.append(str(dist[i][j]))
    print(" ".join(row_output))