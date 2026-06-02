import sys

def gf_mul(a, b):
    r = 0
    for _ in range(8):
        if b & 1:
            r ^= a
        hi = a & 0x80
        a = (a << 1) & 0xff
        if hi:
            a ^= 0x1b
        b >>= 1
    return r

def gf_pow(a, n):
    r = 1
    while n > 0:
        if n & 1:
            r = gf_mul(r, a)
        a = gf_mul(a, a)
        n >>= 1
    return r

def gf_inv(a):
    return gf_pow(a, 254)

# Deterministic PRNG: seed from secret bytes using a simple LCG-like over GF(256)
class DetRand:
    def __init__(self, seed_bytes):
        # SHA-like simple mix using stdlib hashlib
        import hashlib
        h = hashlib.sha256(seed_bytes).digest()
        self.buf = list(h)
        self.idx = 0
        self.h = hashlib.sha256(seed_bytes)
    def next_byte(self):
        if self.idx >= len(self.buf):
            self.h.update(b'x')
            self.buf = list(self.h.digest())
            self.idx = 0
        b = self.buf[self.idx]
        self.idx += 1
        return b

def eval_poly(coeffs, x):
    # coeffs[0] = secret byte, coeffs[i] = coefficient of x^i in GF(256)
    r = 0
    for c in reversed(coeffs):
        r = gf_mul(r, x) ^ c
    return r

def main():
    data = sys.stdin.read().split()
    secret_hex = data[0]
    N = int(data[1])
    K = int(data[2])
    secret = bytes.fromhex(secret_hex)
    rng = DetRand(secret + bytes([N, K]))
    # For each byte of secret, generate K-1 random coefficients
    polys = []
    for sb in secret:
        coeffs = [sb]
        for _ in range(K - 1):
            coeffs.append(rng.next_byte())
        polys.append(coeffs)
    # Generate N shares at x=1..N
    shares = []
    for x in range(1, N + 1):
        share_bytes = bytearray()
        for poly in polys:
            share_bytes.append(eval_poly(poly, x))
        shares.append((x, bytes(share_bytes)))
    out = []
    for x, sb in shares:
        out.append(f"share {x}: {sb.hex()}")
    out.append(f"reconstruction requires any {K} of {N} shares")
    print('\n'.join(out))

main()
