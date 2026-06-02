import sys

P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

def inv(a, m=P):
    return pow(a, m-2, m)

def add(p, q):
    if p is None: return q
    if q is None: return p
    x1,y1 = p; x2,y2 = q
    if x1 == x2:
        if (y1 + y2) % P == 0:
            return None
        m = (3*x1*x1) * inv(2*y1) % P
    else:
        m = (y2 - y1) * inv((x2 - x1) % P) % P
    x3 = (m*m - x1 - x2) % P
    y3 = (m*(x1 - x3) - y1) % P
    return (x3, y3)

def mul(k, p):
    r = None
    while k > 0:
        if k & 1:
            r = add(r, p)
        p = add(p, p)
        k >>= 1
    return r

data = sys.stdin.read().split()
a = int(data[0], 16) % N
b = int(data[1], 16) % N
G = (Gx, Gy)
pubB = mul(b, G)
shared = mul(a, pubB)
print('%064x' % shared[0])
