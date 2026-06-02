import sys, json

def keccak256(data: bytes) -> str:
    # Keccak-f[1600] with rate=1088 bits (136 bytes), pre-NIST padding (0x01 ... 0x80)
    RC = [0x0000000000000001,0x0000000000008082,0x800000000000808A,0x8000000080008000,
          0x000000000000808B,0x0000000080000001,0x8000000080008081,0x8000000000008009,
          0x000000000000008A,0x0000000000000088,0x0000000080008009,0x000000008000000A,
          0x000000008000808B,0x800000000000008B,0x8000000000008089,0x8000000000008003,
          0x8000000000008002,0x8000000000000080,0x000000000000800A,0x800000008000000A,
          0x8000000080008081,0x8000000000008080,0x0000000080000001,0x8000000080008008]
    R = [[0,36,3,41,18],[1,44,10,45,2],[62,6,43,15,61],[28,55,25,21,56],[27,20,39,8,14]]
    def rol(x, n):
        return ((x << n) | (x >> (64 - n))) & 0xFFFFFFFFFFFFFFFF
    def keccak_f(state):
        for rnd in range(24):
            C = [state[x][0]^state[x][1]^state[x][2]^state[x][3]^state[x][4] for x in range(5)]
            D = [C[(x-1)%5] ^ rol(C[(x+1)%5], 1) for x in range(5)]
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
                    state[x][y] &= 0xFFFFFFFFFFFFFFFF
            state[0][0] ^= RC[rnd]
        return state
    rate = 136
    # padding
    data = bytearray(data)
    pad_len = rate - (len(data) % rate)
    if pad_len == 1:
        data.append(0x81)
    else:
        data.append(0x01)
        data.extend(b'\x00' * (pad_len - 2))
        data.append(0x80)
    state = [[0]*5 for _ in range(5)]
    for i in range(0, len(data), rate):
        block = data[i:i+rate]
        for j in range(rate // 8):
            lane = int.from_bytes(block[j*8:(j+1)*8], 'little')
            x = j % 5
            y = j // 5
            state[x][y] ^= lane
        state = keccak_f(state)
    out = b''
    for j in range(4):
        x = j % 5
        y = j // 5
        out += state[x][y].to_bytes(8, 'little')
    return out[:32].hex()

def main():
    data = sys.stdin.read().split('\n')
    sigs = json.loads(data[0])
    events = []
    for line in data[1:]:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if parts[0] != 'EMIT':
            continue
        name = parts[1]
        params = parts[2:]
        types = sigs[name]
        signature = name + '(' + ','.join(types) + ')'
        topic = keccak256(signature.encode('utf-8'))
        events.append({'topic': topic, 'data': params})
    print(json.dumps(events, separators=(',', ':')))

main()
