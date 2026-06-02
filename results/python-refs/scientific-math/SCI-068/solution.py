import sys

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    xs = []
    ys = []
    for _ in range(n):
        xs.append(float(data[idx])); idx += 1
        ys.append(float(data[idx])); idx += 1
    queries = []
    while idx < len(data):
        queries.append(float(data[idx])); idx += 1
    # natural cubic spline
    h = [xs[i+1]-xs[i] for i in range(n-1)]
    # solve tridiagonal for M (second derivatives), M[0]=M[n-1]=0
    # For i=1..n-2: h[i-1]*M[i-1] + 2*(h[i-1]+h[i])*M[i] + h[i]*M[i+1] = 6*((y[i+1]-y[i])/h[i] - (y[i]-y[i-1])/h[i-1])
    M = [0.0]*n
    if n >= 3:
        a = [0.0]*(n-2)
        b = [0.0]*(n-2)
        c = [0.0]*(n-2)
        d = [0.0]*(n-2)
        for i in range(1, n-1):
            k = i-1
            a[k] = h[i-1] if i-1 > 0 else 0.0
            b[k] = 2*(h[i-1]+h[i])
            c[k] = h[i] if i < n-2 else 0.0
            d[k] = 6*((ys[i+1]-ys[i])/h[i] - (ys[i]-ys[i-1])/h[i-1])
        # Thomas algorithm
        m = len(b)
        cp = [0.0]*m
        dp = [0.0]*m
        cp[0] = c[0]/b[0]
        dp[0] = d[0]/b[0]
        for i in range(1, m):
            denom = b[i] - a[i]*cp[i-1]
            cp[i] = c[i]/denom if i < m-1 else 0.0
            dp[i] = (d[i] - a[i]*dp[i-1])/denom
        x_sol = [0.0]*m
        x_sol[m-1] = dp[m-1]
        for i in range(m-2, -1, -1):
            x_sol[i] = dp[i] - cp[i]*x_sol[i+1]
        for i in range(1, n-1):
            M[i] = x_sol[i-1]
    out = []
    for q in queries:
        # find interval
        i = 0
        if q <= xs[0]:
            i = 0
        elif q >= xs[-1]:
            i = n-2
        else:
            lo, hi = 0, n-1
            while lo+1 < hi:
                mid = (lo+hi)//2
                if xs[mid] <= q:
                    lo = mid
                else:
                    hi = mid
            i = lo
        hi_ = h[i]
        A = (xs[i+1]-q)/hi_
        B = (q-xs[i])/hi_
        y = A*ys[i] + B*ys[i+1] + ((A**3 - A)*M[i] + (B**3 - B)*M[i+1])*(hi_*hi_)/6.0
        out.append(f"S({q:g}) = {y:.6f}")
    print('\n'.join(out))

main()
