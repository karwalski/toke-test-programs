import sys, json, hashlib, hmac

# secp256k1 parameters
P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
A = 0
B = 7
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

def inv(a, m):
    return pow(a, -1, m)

def point_add(p1, p2):
    if p1 is None: return p2
    if p2 is None: return p1
    x1,y1 = p1; x2,y2 = p2
    if x1 == x2:
        if (y1 + y2) % P == 0:
            return None
        m = (3*x1*x1) * inv(2*y1, P) % P
    else:
        m = (y2 - y1) * inv(x2 - x1, P) % P
    x3 = (m*m - x1 - x2) % P
    y3 = (m*(x1 - x3) - y1) % P
    return (x3, y3)

def scalar_mul(k, point):
    result = None
    addend = point
    while k:
        if k & 1:
            result = point_add(result, addend)
        addend = point_add(addend, addend)
        k >>= 1
    return result

def rfc6979_k(priv, msg_hash):
    # RFC 6979 deterministic k generation
    x = priv.to_bytes(32, 'big')
    h1 = msg_hash
    V = b'\x01' * 32
    K = b'\x00' * 32
    K = hmac.new(K, V + b'\x00' + x + h1, hashlib.sha256).digest()
    V = hmac.new(K, V, hashlib.sha256).digest()
    K = hmac.new(K, V + b'\x01' + x + h1, hashlib.sha256).digest()
    V = hmac.new(K, V, hashlib.sha256).digest()
    while True:
        V = hmac.new(K, V, hashlib.sha256).digest()
        k = int.from_bytes(V, 'big')
        if 1 <= k < N:
            return k
        K = hmac.new(K, V + b'\x00', hashlib.sha256).digest()
        V = hmac.new(K, V, hashlib.sha256).digest()

def sign(priv, msg_hash):
    z = int.from_bytes(msg_hash, 'big')
    while True:
        k = rfc6979_k(priv, msg_hash)
        R = scalar_mul(k, (Gx, Gy))
        r = R[0] % N
        if r == 0: continue
        s = (inv(k, N) * (z + r * priv)) % N
        if s == 0: continue
        # low-s
        if s > N // 2:
            s = N - s
        return r, s

def main():
    data = sys.stdin.read().split('\n')
    tx = json.loads(data[0])
    priv_hex = data[1].strip()
    priv = int(priv_hex, 16)
    canonical = json.dumps(tx, sort_keys=True, separators=(',', ':'))
    h = hashlib.sha256(canonical.encode()).digest()
    r, s = sign(priv, h)
    sig = r.to_bytes(32, 'big').hex() + s.to_bytes(32, 'big').hex()
    tx['signature'] = sig
    print(json.dumps(tx, sort_keys=True, separators=(',', ':')))

main()
