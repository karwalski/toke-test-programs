import hashlib
import hmac
import sys

P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
GX = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
GY = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

def inv(a, m):
    return pow(a % m, -1, m)

def point_add(P1, P2):
    if P1 is None:
        return P2
    if P2 is None:
        return P1
    x1, y1 = P1
    x2, y2 = P2
    if x1 == x2:
        if (y1 + y2) % P == 0:
            return None
        s = (3 * x1 * x1) * inv(2 * y1, P) % P
    else:
        s = (y2 - y1) * inv(x2 - x1, P) % P
    x3 = (s * s - x1 - x2) % P
    y3 = (s * (x1 - x3) - y1) % P
    return (x3, y3)

def scalar_mult(k, point):
    result = None
    addend = point
    while k:
        if k & 1:
            result = point_add(result, addend)
        addend = point_add(addend, addend)
        k >>= 1
    return result

def rfc6979_k(priv, msg_hash, n):
    qlen = n.bit_length()
    rlen = (qlen + 7) // 8

    def bits2int(b):
        x = int.from_bytes(b, 'big')
        l = len(b) * 8
        if l > qlen:
            x >>= (l - qlen)
        return x

    def int2octets(x):
        return x.to_bytes(rlen, 'big')

    def bits2octets(b):
        z1 = bits2int(b)
        z2 = z1 % n
        return int2octets(z2)

    h1 = msg_hash
    x_oct = int2octets(priv)
    h1_oct = bits2octets(h1)

    hlen = 32
    V = b'\x01' * hlen
    K = b'\x00' * hlen

    K = hmac.new(K, V + b'\x00' + x_oct + h1_oct, hashlib.sha256).digest()
    V = hmac.new(K, V, hashlib.sha256).digest()
    K = hmac.new(K, V + b'\x01' + x_oct + h1_oct, hashlib.sha256).digest()
    V = hmac.new(K, V, hashlib.sha256).digest()

    while True:
        T = b''
        while len(T) < rlen:
            V = hmac.new(K, V, hashlib.sha256).digest()
            T += V
        k = bits2int(T)
        if 1 <= k < n:
            return k
        K = hmac.new(K, V + b'\x00', hashlib.sha256).digest()
        V = hmac.new(K, V, hashlib.sha256).digest()

def main():
    data = sys.stdin.read().split('\n')
    priv_hex = data[0].strip()
    message = data[1] if len(data) > 1 else ''

    priv = int(priv_hex, 16)
    msg_hash = hashlib.sha256(message.encode()).digest()
    z = int.from_bytes(msg_hash, 'big')

    while True:
        k = rfc6979_k(priv, msg_hash, N)
        R = scalar_mult(k, (GX, GY))
        r = R[0] % N
        if r == 0:
            continue
        s = (inv(k, N) * (z + r * priv)) % N
        if s == 0:
            continue
        break

    print(f"r={r:064x}")
    print(f"s={s:064x}")

main()