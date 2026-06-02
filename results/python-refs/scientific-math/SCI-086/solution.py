import sys

def generate_pascals_triangle(n):
    triangle = []
    for i in range(n):
        row = [1] * (i + 1)
        for j in range(1, i):
            row[j] = triangle[i-1][j-1] + triangle[i-1][j]
        triangle.append(row)
    return triangle

def get_binomial_coefficient(triangle, n, k):
    if n < len(triangle) and k < len(triangle[n]):
        return triangle[n][k]
    return 0

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.strip())

n = int(lines[0])
triangle = generate_pascals_triangle(n)

# Print Pascal's triangle
for row in triangle:
    print(' '.join(map(str, row)))

# Handle optional query
if len(lines) > 1:
    parts = lines[1].split()
    query_n = int(parts[0])
    query_k = int(parts[1])
    result = get_binomial_coefficient(triangle, query_n, query_k)
    print(f"C({query_n},{query_k}) = {result}")