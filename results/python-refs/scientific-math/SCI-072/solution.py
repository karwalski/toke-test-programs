import sys, math

def main():
    data = sys.stdin.read().split('\n')
    idx = 0
    n = int(data[idx].strip()); idx += 1
    A = []
    for i in range(n):
        row = list(map(float, data[idx].split())); idx += 1
        A.append(row)
    max_iter = int(data[idx].strip()); idx += 1
    tol = float(data[idx].strip()); idx += 1

    v = [1.0]*n
    norm = math.sqrt(sum(x*x for x in v))
    v = [x/norm for x in v]
    prev_eig = 0.0
    out_lines = []
    eig = 0.0
    for it in range(1, max_iter+1):
        w = [sum(A[i][j]*v[j] for j in range(n)) for i in range(n)]
        norm = math.sqrt(sum(x*x for x in w))
        if norm == 0:
            break
        v_new = [x/norm for x in w]
        eig = sum(v_new[i]*sum(A[i][j]*v_new[j] for j in range(n)) for i in range(n))
        out_lines.append('Iteration {}: eigenvalue={:.6f}'.format(it, eig))
        v = v_new
        if abs(eig - prev_eig) < tol:
            break
        prev_eig = eig

    # Sign convention: make first nonzero component positive
    for x in v:
        if abs(x) > 1e-12:
            if x < 0:
                v = [-y for y in v]
            break

    print('\n'.join(out_lines))
    print('Dominant eigenvalue: {:.6f}'.format(eig))
    print('Eigenvector: ' + ' '.join('{:.6f}'.format(x) for x in v))

main()
