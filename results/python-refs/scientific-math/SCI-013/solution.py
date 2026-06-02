import sys, math

def main():
    data = sys.stdin.read().split()
    idx = 0
    m = int(data[idx]); idx+=1
    n = int(data[idx]); idx+=1
    A = []
    for i in range(m):
        row = [float(data[idx+j]) for j in range(n)]
        idx += n
        A.append(row)
    # columns of A
    cols = [[A[i][j] for i in range(m)] for j in range(n)]
    Q = [[0.0]*n for _ in range(m)]
    R = [[0.0]*n for _ in range(n)]
    qcols = []
    for j in range(n):
        v = list(cols[j])
        for i in range(j):
            q = qcols[i]
            r = sum(q[k]*cols[j][k] for k in range(m))
            R[i][j] = r
            for k in range(m):
                v[k] -= r*q[k]
        norm = math.sqrt(sum(x*x for x in v))
        R[j][j] = norm
        if norm == 0:
            qcols.append([0.0]*m)
        else:
            qcols.append([x/norm for x in v])
    for i in range(m):
        for j in range(n):
            Q[i][j] = qcols[j][i]
    out = []
    for i in range(m):
        out.append(' '.join(f'{Q[i][j]:.6f}' for j in range(n)))
    out.append('')
    for i in range(n):
        out.append(' '.join(f'{R[i][j]:.6f}' for j in range(n)))
    print('\n'.join(out))

main()
