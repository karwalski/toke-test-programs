# Keccak-256 implementation (not SHA3-256, which differs in padding)

def keccak_256(data: bytes) -> bytes:
    # Keccak-f[1600] permutation
    RC = [
        0x0000000000000001, 0x0000000000008082, 0x800000000000808A,
        0x8000000080008000, 0x000000000000808B, 0x0000000080000001,
        0x8000000080008081, 0x8000000000008009, 0x000000000000008A,
        0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
        0x000000008000808B, 0x800000000000008B, 0x8000000000008089,
        0x8000000000008003, 0x8000000000008002, 0x8000000000000080,
        0x000000000000800A, 0x800000008000000A, 0x8000000080008081,
        0x8000000000008080, 0x0000000080000001, 0x8000000080008008,
    ]
    r = [
        [0, 36, 3, 41, 18],
        [1, 44, 10, 45, 2],
        [62, 6, 43, 15, 61],
        [28, 55, 25, 21, 56],
        [27, 20, 39, 8, 14],
    ]

    def rol(x, n):
        return ((x << n) | (x >> (64 - n))) & 0xFFFFFFFFFFFFFFFF

    def keccak_f(state):
        for rnd in range(24):
            # Theta
            C = [state[x][0] ^ state[x][1] ^ state[x][2] ^ state[x][3] ^ state[x][4] for x in range(5)]
            D = [C[(x - 1) % 5] ^ rol(C[(x + 1) % 5], 1) for x in range(5)]
            for x in range(5):
                for y in range(5):
                    state[x][y] ^= D[x]
            # Rho and Pi
            B = [[0] * 5 for _ in range(5)]
            for x in range(5):
                for y in range(5):
                    B[y][(2 * x + 3 * y) % 5] = rol(state[x][y], r[x][y])
            # Chi
            for x in range(5):
                for y in range(5):
                    state[x][y] = B[x][y] ^ ((~B[(x + 1) % 5][y]) & B[(x + 2) % 5][y]) & 0xFFFFFFFFFFFFFFFF
            # Iota
            state[0][0] ^= RC[rnd]
        return state

    rate = 136  # bytes (1088 bits) for Keccak-256
    # Padding: Keccak (not SHA-3) uses 0x01 ... 0x80
    data = bytearray(data)
    pad_len = rate - (len(data) % rate)
    if pad_len == 1:
        data.append(0x81)
    else:
        data.append(0x01)
        data.extend([0x00] * (pad_len - 2))
        data.append(0x80)

    state = [[0] * 5 for _ in range(5)]
    for block_start in range(0, len(data), rate):
        block = data[block_start:block_start + rate]
        for i in range(rate // 8):
            lane = int.from_bytes(block[i * 8:(i + 1) * 8], 'little')
            x = i % 5
            y = i // 5
            state[x][y] ^= lane
        state = keccak_f(state)

    out = bytearray()
    for i in range(4):  # 32 bytes = 4 lanes
        x = i % 5
        y = i // 5
        out.extend(state[x][y].to_bytes(8, 'little'))
    return bytes(out)


address = input().strip().lower()
h = keccak_256(address.encode('ascii')).hex()

result = ""
for i, c in enumerate(address):
    if c in "0123456789":
        result += c
    else:
        if int(h[i], 16) >= 8:
            result += c.upper()
        else:
            result += c

print("0x" + result)