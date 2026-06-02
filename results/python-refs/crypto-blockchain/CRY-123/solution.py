import sys, json

def keccak_f(state):
    RC = [0x0000000000000001,0x0000000000008082,0x800000000000808A,0x8000000080008000,
          0x000000000000808B,0x0000000080000001,0x8000000080008081,0x8000000000008009,
          0x000000000000008A,0x0000000000000088,0x0000000080008009,0x000000008000000A,
          0x000000008000808B,0x800000000000008B,0x8000000000008089,0x8000000000008003,
          0x8000000000008002,0x8000000000000080,0x000000000000800A,0x800000008000000A,
          0x8000000080008081,0x8000000000008080,0x0000000080000001,0x8000000080008008]
    R = [[0,36,3,41,18],[1,44,10,45,2],[62,6,43,15,61],[28,55,25,21,56],[27,20,39,8,14]]
    def rol(x,n): return ((x<<n)|(x>>(64-n)))&0xFFFFFFFFFFFFFFFF
    A = [[state[x+5*y] for y in range(5)] for x in range(5)]
    for rnd in range(24):
        C = [A[x][0]^A[x][1]^A[x][2]^A[x][3]^A[x][4] for x in range(5)]
        D = [C[(x-1)%5]^rol(C[(x+1)%5],1) for x in range(5)]
        for x in range(5):
            for y in range(5):
                A[x][y] ^= D[x]
        B = [[0]*5 for _ in range(5)]
        for x in range(5):
            for y in range(5):
                B[y][(2*x+3*y)%5] = rol(A[x][y], R[x][y])
        for x in range(5):
            for y in range(5):
                A[x][y] = B[x][y] ^ ((~B[(x+1)%5][y]) & B[(x+2)%5][y]) & 0xFFFFFFFFFFFFFFFF
        A[0][0] ^= RC[rnd]
    return [A[x][y] for y in range(5) for x in range(5)]

def keccak256(data):
    rate = 136
    state = [0]*25
    # pad with 0x01 (Keccak original padding)
    padded = data + b'\x01'
    while len(padded) % rate != 0:
        padded += b'\x00'
    padded = padded[:-1] + bytes([padded[-1] | 0x80])
    for i in range(0, len(padded), rate):
        block = padded[i:i+rate]
        for j in range(rate//8):
            state[j] ^= int.from_bytes(block[j*8:(j+1)*8], 'little')
        state = keccak_f(state)
    out = b''
    for j in range(4):
        out += state[j].to_bytes(8, 'little')
    return out

def rlp_encode_bytes(b):
    if len(b) == 1 and b[0] < 0x80:
        return b
    if len(b) < 56:
        return bytes([0x80+len(b)]) + b
    l = len(b).to_bytes((len(b).bit_length()+7)//8, 'big')
    return bytes([0xb7+len(l)]) + l + b

def rlp_encode_list(items):
    payload = b''.join(items)
    if len(payload) < 56:
        return bytes([0xc0+len(payload)]) + payload
    l = len(payload).to_bytes((len(payload).bit_length()+7)//8, 'big')
    return bytes([0xf7+len(l)]) + l + payload

def encode_int(n):
    if n == 0:
        return rlp_encode_bytes(b'')
    b = n.to_bytes((n.bit_length()+7)//8, 'big')
    return rlp_encode_bytes(b)

def encode_hex(s):
    if s.startswith('0x'):
        s = s[2:]
    if s == '':
        return rlp_encode_bytes(b'')
    if len(s) % 2 == 1:
        s = '0' + s
    return rlp_encode_bytes(bytes.fromhex(s))

def main():
    lines = sys.stdin.read().splitlines()
    tx = json.loads(lines[0])
    chain_id = int(lines[1].strip())
    items = [
        encode_int(tx['nonce']),
        encode_int(tx['gas_price']),
        encode_int(tx['gas_limit']),
        encode_hex(tx['to']),
        encode_int(tx['value']),
        encode_hex(tx['data']) if isinstance(tx['data'], str) else rlp_encode_bytes(b''),
        encode_int(chain_id),
        encode_int(0),
        encode_int(0),
    ]
    rlp = rlp_encode_list(items)
    h = keccak256(rlp)
    print(h.hex())

main()
