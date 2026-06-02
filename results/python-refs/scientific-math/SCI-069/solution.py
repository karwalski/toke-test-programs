import sys

def main():
    data = sys.stdin.read().split('\n')
    coeffs = [float(c) for c in data[0].split()]
    x = float(data[1])
    lr = float(data[2])
    tol = float(data[3])
    max_iters = int(data[4])

    def f(x):
        return sum(c * (x ** i) for i, c in enumerate(coeffs))
    def grad(x):
        return sum(i * c * (x ** (i - 1)) for i, c in enumerate(coeffs) if i >= 1)

    diverged = False
    out = []
    for it in range(1, max_iters + 1):
        g = grad(x)
        fx = f(x)
        out.append('Iter {}: x={:.6f} f(x)={:.6f} grad={:.6f}'.format(it, x, fx, g))
        if abs(g) < tol:
            break
        x_new = x - lr * g
        if not (abs(x_new) < 1e12) or x_new != x_new:
            diverged = True
            break
        x = x_new

    if diverged:
        print('\n'.join(out))
        print('DIVERGED')
    else:
        print('\n'.join(out))
        print('Minimum: x={:.6f} f(x)={:.6f}'.format(x, f(x)))

main()
