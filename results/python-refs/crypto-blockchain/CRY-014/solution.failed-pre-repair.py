import sys

def keccak_f(state):
    """Keccak-f[1600] permutation"""
    # Round constants
    RC = [
        0x0000000000000001, 0x0000000000008082, 0x800000000000808a, 0x8000000080008000,
        0x000000000000808b, 0x0000000080000001, 0x8000000080008081, 0x8000000000008009,
        0x000000000000008a, 0x0000000000000088, 0x0000000080008009, 0x000000008000000a,
        0x000000008000808b, 0x800000000000008b, 0x8000000000008089, 0x8000000000008003,
        0x8000000000008002, 0x8000000000000080, 0x000000000000800a, 0x800000008000000a,
        0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008
    ]
    
    # Rotation offsets
    r = [0, 1, 62, 28, 27, 36, 44, 6, 55, 20, 3, 10, 43, 25, 39, 41, 45, 15, 21, 8, 18, 2, 61, 56, 14]
    
    def rotl64(x, n):
        return ((x << n) | (x >> (64 - n))) & 0xffffffffffffffff
    
    # Convert state to 5x5 array of 64-bit lanes
    A = [[0] * 5 for _ in range(5)]
    for i in range(25):
        A[i // 5][i % 5] = state[i]
    
    for round_num in range(24):
        # θ (Theta)
        C = [A[0][x] ^ A[1][x] ^ A[2][x] ^ A[3][x] ^ A[4][x] for x in range(5)]
        D = [C[(x + 4) % 5] ^ rotl64(C[(x + 1) % 5], 1) for x in range(5)]
        for y in range(5):
            for x in range(5):
                A[y][x] ^= D[x]
        
        # ρ (Rho) and π (Pi)
        B = [[0] * 5 for _ in range(5)]
        for y in range(5):
            for x in range(5):
                B[y][(2*x + 3*y) % 5] = rotl64(A[y][x], r[5*y + x])
        
        # χ (Chi)
        for y in range(5):
            for x in range(5):
                A[y][x] = B[y][x] ^ (~B[y][(x + 1) % 5] & B[y][(x + 2) % 5])
                A[y][x] &= 0xffffffffffffffff
        
        # ι (Iota)
        A[0][0] ^= RC[round_num]
    
    # Convert back to flat array
    for i in range(25):
        state[i] = A[i // 5][i % 5]
    
    return state

def keccak256(data):
    """Keccak-256 hash function"""
    # Initialize state (25 64-bit words = 1600 bits)
    state = [0] * 25
    
    # Rate for Keccak-256 is 1088 bits = 136 bytes
    rate = 136
    
    # Padding and absorption
    padded = data + b'\x01'
    while len(padded) % rate != (rate - 1):
        padded += b'\x00'
    padded += b'\x80'
    
    # Process each block
    for i in range(0, len(padded), rate):
        block = padded[i:i + rate]
        
        # XOR block into state
        for j in range(0, len(block), 8):
            if j + 8 <= len(block):
                word = int.from_bytes(block[j:j + 8], 'little')
                state[j // 8] ^= word
        
        # Apply Keccak-f permutation
        state = keccak_f(state)
    
    # Extract 32 bytes (256 bits) for output
    output = b''
    for i in range(4):  # 32 bytes = 4 * 8 bytes
        output += state[i].to_bytes(8, 'little')
    
    return output[:32]

# Read input
text = sys.stdin.read().strip()
data = text.encode('utf-8')

# Compute Keccak-256 hash
hash_bytes = keccak256(data)

# Output as lowercase hex
print(hash_bytes.hex())