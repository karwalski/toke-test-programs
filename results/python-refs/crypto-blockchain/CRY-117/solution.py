import sys

def keccak256(data):
    # Keccak-256 implementation
    RC = [0x0000000000000001,0x0000000000008082,0x800000000000808A,0x8000000080008000,
          0x000000000000808B,0x0000000080000001,0x8000000080008081,0x8000000000008009,
          0x000000000000008A,0x0000000000000088,0x0000000080008009,0x000000008000000A,
          0x000000008000808B,0x800000000000008B,0x8000000000008089,0x8000000000008003,
          0x8000000000008002,0x8000000000000080,0x000000000000800A,0x800000008000000A,
          0x8000000080008081,0x8000000000008080,0x0000000080000001,0x8000000080008008]
    R = [[0,36,3,41,18],[1,44,10,45,2],[62,6,43,15,61],[28,55,25,21,56],[27,20,39,8,14]]
    def rol(x,n): return ((x<<n)|(x>>(64-n)))&0xFFFFFFFFFFFFFFFF
    rate = 136
    state = [[0]*5 for _ in range(5)]
    # padding: append 0x01, then 0x00*, then last byte |= 0x80
    data = bytearray(data)
    pad_len = rate - (len(data) % rate)
    if pad_len == 1:
        data.append(0x81)
    else:
        data.append(0x01)
        data.extend([0]*(pad_len-2))
        data.append(0x80)
    for block_start in range(0, len(data), rate):
        block = data[block_start:block_start+rate]
        for i in range(rate//8):
            lane = int.from_bytes(block[i*8:i*8+8], 'little')
            x = i % 5
            y = i // 5
            state[x][y] ^= lane
        # Keccak-f[1600]
        for rnd in range(24):
            C = [state[x][0]^state[x][1]^state[x][2]^state[x][3]^state[x][4] for x in range(5)]
            D = [C[(x-1)%5] ^ rol(C[(x+1)%5],1) for x in range(5)]
            for x in range(5):
                for y in range(5):
                    state[x][y] ^= D[x]
            B = [[0]*5 for _ in range(5)]
            for x in range(5):
                for y in range(5):
                    B[y][(2*x+3*y)%5] = rol(state[x][y], R[x][y])
            for x in range(5):
                for y in range(5):
                    state[x][y] = B[x][y] ^ ((~B[(x+1)%5][y]) & B[(x+2)%5][y]) & 0xFFFFFFFFFFFFFFFF
            state[0][0] ^= RC[rnd]
    out = bytearray()
    while len(out) < 32:
        for i in range(rate//8):
            x = i % 5
            y = i // 5
            out.extend(state[x][y].to_bytes(8,'little'))
            if len(out) >= 32:
                break
    return bytes(out[:32])

def parse_sig(sig):
    name, rest = sig.split('(', 1)
    args = rest.rstrip(')')
    if args == '':
        return name, []
    return name, args.split(',')

def encode_arg(t, v):
    if t == 'address':
        h = v.lower()
        if h.startswith('0x'): h = h[2:]
        return bytes.fromhex(h.rjust(64, '0'))
    elif t.startswith('uint') or t.startswith('int'):
        n = int(v)
        if n < 0:
            n = n & ((1<<256)-1)
        return n.to_bytes(32, 'big')
    elif t == 'bool':
        return (1 if v.lower() in ('true','1') else 0).to_bytes(32,'big')
    else:
        raise ValueError('unsupported type: '+t)

def main():
    lines = sys.stdin.read().split('\n')
    sig = lines[0].strip()
    name, types = parse_sig(sig)
    selector = keccak256(sig.encode())[:4]
    out = selector
    for i, t in enumerate(types):
        v = lines[1+i].strip()
        out += encode_arg(t, v)
    print(out.hex())

main()
