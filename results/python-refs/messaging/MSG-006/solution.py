import sys, hashlib

p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
a = -3 % p
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
Gx = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
Gy = 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5
n = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551

def inv(x, m):
    return pow(x, -1, m)

def pt_add(P, Q):
    if P is None: return Q
    if Q is None: return P
    x1,y1 = P; x2,y2 = Q
    if x1 == x2:
        if (y1 + y2) % p == 0:
            return None
        m = (3*x1*x1 + a) * inv(2*y1 % p, p) % p
    else:
        m = (y2 - y1) * inv((x2 - x1) % p, p) % p
    x3 = (m*m - x1 - x2) % p
    y3 = (m*(x1 - x3) - y1) % p
    return (x3, y3)

def scalar_mul(k, P):
    R = None
    Q = P
    while k > 0:
        if k & 1:
            R = pt_add(R, Q)
        Q = pt_add(Q, Q)
        k >>= 1
    return R

def main():
    lines = sys.stdin.read().strip().split('\n')
    a_priv = int(lines[0].strip(), 16)
    b_priv = int(lines[1].strip(), 16)
    if not (1 <= a_priv < n) or not (1 <= b_priv < n):
        sys.exit(1)
    G = (Gx, Gy)
    A = scalar_mul(a_priv, G)
    B = scalar_mul(b_priv, G)
    S = scalar_mul(a_priv, B)
    a_pub = '04' + format(A[0], '064x') + format(A[1], '064x')
    b_pub = '04' + format(B[0], '064x') + format(B[1], '064x')
    shared = format(S[0], '064x')
    aes_key = hashlib.sha256(bytes.fromhex(shared)).hexdigest()
    print(a_pub)
    print(b_pub)
    print(shared)
    print(aes_key)

main()
