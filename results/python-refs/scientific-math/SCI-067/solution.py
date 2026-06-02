import sys

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    xs = []
    ys = []
    for i in range(n):
        x = float(data[idx]); idx += 1
        y = float(data[idx]); idx += 1
        xs.append(x)
        ys.append(y)
    queries = []
    while idx < len(data):
        queries.append(float(data[idx])); idx += 1
    # Build divided difference table
    table = [[0.0]*n for _ in range(n)]
    for i in range(n):
        table[i][0] = ys[i]
    for j in range(1, n):
        for i in range(n-j):
            table[i][j] = (table[i+1][j-1] - table[i][j-1]) / (xs[i+j] - xs[i])
    # Print divided difference table
    print("Divided Difference Table:")
    for i in range(n):
        row = ["{:.6f}".format(xs[i])]
        for j in range(n-i):
            row.append("{:.6f}".format(table[i][j]))
        print(" ".join(row))
    # Coefficients are table[0][0..n-1]
    coeffs = [table[0][j] for j in range(n)]
    for q in queries:
        # Newton's form evaluation
        result = coeffs[n-1]
        for k in range(n-2, -1, -1):
            result = result * (q - xs[k]) + coeffs[k]
        print("p({:g}) = {:.6f}".format(q, result))

main()
