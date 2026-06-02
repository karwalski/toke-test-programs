import sys, csv, json, io

def solve():
    data = sys.stdin.read()
    reader = csv.reader(io.StringIO(data))
    rows = [r for r in reader if r and any(c.strip() for c in r)]
    header = rows[0]
    nfeat = len(header) - 1
    X = []
    y = []
    for r in rows[1:]:
        vals = [float(v) for v in r]
        X.append(vals[:nfeat])
        y.append(vals[nfeat])
    n = len(X)
    # Build design matrix with intercept column
    A = [[1.0] + row for row in X]
    m = nfeat + 1
    # Compute A^T A and A^T y
    ATA = [[0.0]*m for _ in range(m)]
    ATy = [0.0]*m
    for i in range(n):
        for j in range(m):
            ATy[j] += A[i][j] * y[i]
            for k in range(m):
                ATA[j][k] += A[i][j] * A[i][k]
    # Solve via Gaussian elimination
    M = [ATA[i][:] + [ATy[i]] for i in range(m)]
    for i in range(m):
        # pivot
        pivot = i
        for r in range(i+1, m):
            if abs(M[r][i]) > abs(M[pivot][i]):
                pivot = r
        M[i], M[pivot] = M[pivot], M[i]
        if abs(M[i][i]) < 1e-12:
            # singular - skip
            continue
        for r in range(m):
            if r != i and abs(M[r][i]) > 1e-15:
                f = M[r][i] / M[i][i]
                for c in range(i, m+1):
                    M[r][c] -= f * M[i][c]
    beta = [M[i][m] / M[i][i] if abs(M[i][i]) > 1e-12 else 0.0 for i in range(m)]
    intercept = beta[0]
    coefs = beta[1:]
    # r_squared
    ymean = sum(y)/n
    ss_tot = sum((yi - ymean)**2 for yi in y)
    ss_res = 0.0
    for i in range(n):
        pred = intercept + sum(coefs[j]*X[i][j] for j in range(nfeat))
        ss_res += (y[i] - pred)**2
    if ss_tot < 1e-15:
        r2 = 1.0
    else:
        r2 = 1.0 - ss_res/ss_tot
    out = {
        "coefficients": [round(c, 4) for c in coefs],
        "intercept": round(intercept, 4),
        "r_squared": round(r2, 4)
    }
    print(json.dumps(out))

solve()
