import sys, json, hashlib

P = 19
M = 784931

def siphash(key, data):
    # SipHash-2-4 implementation
    assert len(key) == 16
    k0 = int.from_bytes(key[0:8], 'little')
    k1 = int.from_bytes(key[8:16], 'little')
    v0 = k0 ^ 0x736f6d6570736575
    v1 = k1 ^ 0x646f72616e646f6d
    v2 = k0 ^ 0x6c7967656e657261
    v3 = k1 ^ 0x7465646279746573
    MASK = (1<<64)-1
    def rotl(x,b): return ((x<<b)|(x>>(64-b))) & MASK
    def sipround():
        nonlocal v0,v1,v2,v3
        v0=(v0+v1)&MASK; v1=rotl(v1,13); v1^=v0; v0=rotl(v0,32)
        v2=(v2+v3)&MASK; v3=rotl(v3,16); v3^=v2
        v0=(v0+v3)&MASK; v3=rotl(v3,21); v3^=v0
        v2=(v2+v1)&MASK; v1=rotl(v1,17); v1^=v2; v2=rotl(v2,32)
    length = len(data)
    i = 0
    while i + 8 <= length:
        m = int.from_bytes(data[i:i+8], 'little')
        v3 ^= m
        sipround(); sipround()
        v0 ^= m
        i += 8
    last = length & 0xff
    tail = data[i:]
    b = (last << 56) & MASK
    for j,byte in enumerate(tail):
        b |= byte << (8*j)
    v3 ^= b
    sipround(); sipround()
    v0 ^= b
    v2 ^= 0xff
    sipround(); sipround(); sipround(); sipround()
    return (v0 ^ v1 ^ v2 ^ v3) & MASK

def hash_to_range(item, F, key):
    h = siphash(key, item)
    return (h * F) >> 64

def hashed_set_construct(items, N, key):
    F = N * M
    return sorted(hash_to_range(it, F, key) for it in items)

class BitWriter:
    def __init__(self):
        self.bits = []
    def write(self, val, n):
        for i in range(n-1, -1, -1):
            self.bits.append((val >> i) & 1)
    def write_unary(self, q):
        for _ in range(q):
            self.bits.append(1)
        self.bits.append(0)
    def bytes(self):
        # pad to byte boundary with zeros
        b = self.bits[:]
        while len(b) % 8 != 0:
            b.append(0)
        out = bytearray()
        for i in range(0, len(b), 8):
            byte = 0
            for j in range(8):
                byte = (byte << 1) | b[i+j]
            out.append(byte)
        return bytes(out)

class BitReader:
    def __init__(self, data):
        self.data = data
        self.pos = 0
        self.total = len(data)*8
    def read(self, n):
        v = 0
        for _ in range(n):
            if self.pos >= self.total:
                return None
            byte = self.data[self.pos // 8]
            bit = (byte >> (7 - (self.pos % 8))) & 1
            v = (v << 1) | bit
            self.pos += 1
        return v
    def read_unary(self):
        q = 0
        while True:
            if self.pos >= self.total:
                return None
            byte = self.data[self.pos // 8]
            bit = (byte >> (7 - (self.pos % 8))) & 1
            self.pos += 1
            if bit == 0:
                return q
            q += 1

def encode_gcs(sorted_values, P):
    w = BitWriter()
    last = 0
    for v in sorted_values:
        delta = v - last
        last = v
        q = delta >> P
        r = delta & ((1 << P) - 1)
        w.write_unary(q)
        w.write(r, P)
    return w.bytes()

def compact_size(n):
    if n < 0xfd:
        return bytes([n])
    elif n <= 0xffff:
        return bytes([0xfd]) + n.to_bytes(2, 'little')
    elif n <= 0xffffffff:
        return bytes([0xfe]) + n.to_bytes(4, 'little')
    else:
        return bytes([0xff]) + n.to_bytes(8, 'little')

def decode_and_check(filter_bytes, N, target_hash, P):
    # skip compact size prefix
    br = BitReader(filter_bytes)
    # read compact size
    first = filter_bytes[0]
    if first < 0xfd:
        offset = 1
    elif first == 0xfd:
        offset = 3
    elif first == 0xfe:
        offset = 5
    else:
        offset = 9
    br = BitReader(filter_bytes[offset:])
    last = 0
    for _ in range(N):
        q = br.read_unary()
        if q is None: return False
        r = br.read(P)
        if r is None: return False
        delta = (q << P) | r
        last += delta
        if last == target_hash:
            return True
        if last > target_hash:
            return False
    return False

def main():
    data = sys.stdin.read().split('\n')
    elements = json.loads(data[0])
    query = data[1]
    # Derive a fixed key (BIP158 uses block hash first 16 bytes; we use sha256 of fixed string)
    key = hashlib.sha256(b'CRY-134-FIXED-KEY').digest()[:16]
    elem_bytes = [e.encode('utf-8') for e in elements]
    N = len(elem_bytes)
    hashes = hashed_set_construct(elem_bytes, N, key)
    body = encode_gcs(hashes, P)
    filter_bytes = compact_size(N) + body
    print(filter_bytes.hex())
    # check membership
    F = N * M
    qh = hash_to_range(query.encode('utf-8'), F, key)
    match = decode_and_check(filter_bytes, N, qh, P)
    print('MATCH' if match else 'NO_MATCH')

main()
