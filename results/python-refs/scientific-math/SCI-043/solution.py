import sys

def main():
    data = sys.stdin.read().splitlines()
    coeffs = [float(x) for x in data[0].split()]
    x = float(data[1])
    tol = float(data[2])
    maxit = int(data[3])
    # derivative
    dcoeffs = [i*coeffs[i] for i in range(1, len(coeffs))]
    def f(x):
        r = 0.0
        for c in reversed(coeffs):
            r = r*x + c
        return r
    def df(x):
        r = 0.0
        for c in reversed(dcoeffs):
            r = r*x + c
        return r
    out = []
    converged = False
    iters = 0
    for i in range(1, maxit+1):
        fx = f(x)
        out.append("Iteration {}: x={:.6f} f(x)={:.6f}".format(i, x, fx))
        if abs(fx) < tol:
            converged = True
            iters = i
            break
        dfx = df(x)
        if dfx == 0:
            break
        x = x - fx/dfx
        iters = i
    if converged:
        out.append("Root: {:.6f} ({} iterations)".format(x, iters))
    else:
        out.append("DIVERGED")
    sys.stdout.write("\n".join(out) + "\n")

main()
