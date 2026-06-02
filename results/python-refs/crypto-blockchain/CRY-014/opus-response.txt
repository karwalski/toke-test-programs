import sys

def keccak_f(state):
    RC = [
        0x0000000000000001, 0x0000000000008082, 0x800000000000808a, 0x8000000080008000,
        0x000000000000808b, 0x0000000080000001, 0x8000000080008081, 0x8000000000008009,
        0x000000000000008a, 0x0000000000000088, 0x0000000080008009, 0x000000008000000a,
        0x000000008000808b, 0x800000000000008b, 0x8000000000008089, 0x8000000000008003,
        0x8000000000008002, 0x8000000000000080, 0x000000000000800a, 0x800000008000000a,
        0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008
    ]
    
    r = [[0, 36, 3, 41, 18],
         [1, 44, 10, 45, 2],
         [62, 6, 43, 15, 61],
         [28, 55, 25, 21, 56],
         [27, 20, 39, 8, 14]]
    
    def rotl64(x, n):
        n = n % 64
        return ((x << n) | (x >> (64 - n))) & 0xffffffffffffffff
    
    A = [[0] * 5 for _ in range(5)]
    for x in range(5):
        for y in range(5):
            A[x][y] = state[x + 5 * y]
    
    for round_num in range(24):
        C = [A[x][0] ^ A[x][1] ^ A[x][2] ^ A[x][3] ^ A[x][4] for x in range(5)]
        D = [C[(x + 4) % 5] ^ rotl64(C[(x + 1) % 5], 1) for x in range(5)]
        for x in range(5):
            for y in range(5):
                A[x][y] ^= D[x]
        
        B = [[0] * 5 for _ in range(5)]
        for x in range(5):
            for y in range(5):
                B[y][(2*x + 3*y) % 5] = rotl64(A[x][y], r[x][y])
        
        for x in range(5):
            for y in range(5):
                A[x][y] = B[x][y] ^ ((~B[(x + 1) % 5][y]) & B[(x + 2) % 5][y])
                A[x][y] &= 0xffffffffffffffff
        
        A[0][0] ^= RC[round_num]
    
    for x in range(5):
        for y in range(5):
            state[x + 5 * y] = A[x][y]
    
    return state

def keccak256(data):
    state = [0] * 25
    rate = 136
    
    padded = bytearray(data)
    padded.append(0x01)
    while len(padded) % rate != (rate - 1):
        padded.append(0x00)
    padded.append(0x80)
    
    for i in range(0, len(padded), rate):
        block = padded[i:i + rate]
        for j in range(0, rate, 8):
            word = int.from_bytes(block[j:j + 8], 'little')
            state[j // 8] ^= word
        state = keccak_f(state)
    
    output = b''
    for i in range(4):
        output += state[i].to_bytes(8, 'little')
    
    return output[:32]

data = sys.stdin.buffer.read()
if data.endswith(b'\n'):
    data = data[:-1]
if data.endswith(b'\r'):
    data = data[:-1]

hash_bytes = keccak256(data)
print(hash_bytes.hex())