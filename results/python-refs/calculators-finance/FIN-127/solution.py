import sys

def main():
    data = sys.stdin.read().strip().split('\n')
    rows = [[float(x) for x in line.split(',')] for line in data if line.strip()]
    n = len(rows[0])
    k = len(rows)
    means = [sum(r)/n for r in rows]
    cov = [[0.0]*k for _ in range(k)]
    for i in range(k):
        for j in range(k):
            s = sum((rows[i][t]-means[i])*(rows[j][t]-means[j]) for t in range(n))
            cov[i][j] = s/(n-1)
    out = []
    for i in range(k):
        out.append(' '.join(f'{cov[i][j]:.6f}' for j in range(k)))
    print('\n'.join(out))

main()
