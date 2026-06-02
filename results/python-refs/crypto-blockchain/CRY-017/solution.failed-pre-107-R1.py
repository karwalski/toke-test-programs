import hashlib
import sys

def scrypt(password, salt, N, r, p, dkLen):
    """
    Simple scrypt implementation using only Python stdlib
    """
    def salsa20_8(x):
        """Salsa20/8 core function"""
        def rotl(a, b):
            return ((a << b) | (a >> (32 - b))) & 0xffffffff
        
        x = list(x)
        for i in range(4):
            x[ 4] ^= rotl((x[ 0] + x[12]) & 0xffffffff, 7)
            x[ 8] ^= rotl((x[ 4] + x[ 0]) & 0xffffffff, 9)
            x[12] ^= rotl((x[ 8] + x[ 4]) & 0xffffffff, 13)
            x[ 0] ^= rotl((x[12] + x[ 8]) & 0xffffffff, 18)
            x[ 9] ^= rotl((x[ 5] + x[ 1]) & 0xffffffff, 7)
            x[13] ^= rotl((x[ 9] + x[ 5]) & 0xffffffff, 9)
            x[ 1] ^= rotl((x[13] + x[ 9]) & 0xffffffff, 13)
            x[ 5] ^= rotl((x[ 1] + x[13]) & 0xffffffff, 18)
            x[14] ^= rotl((x[10] + x[ 6]) & 0xffffffff, 7)
            x[ 2] ^= rotl((x[14] + x[10]) & 0xffffffff, 9)
            x[ 6] ^= rotl((x[ 2] + x[14]) & 0xffffffff, 13)
            x[10] ^= rotl((x[ 6] + x[ 2]) & 0xffffffff, 18)
            x[ 3] ^= rotl((x[15] + x[11]) & 0xffffffff, 7)
            x[ 7] ^= rotl((x[ 3] + x[15]) & 0xffffffff, 9)
            x[11] ^= rotl((x[ 7] + x[ 3]) & 0xffffffff, 13)
            x[15] ^= rotl((x[11] + x[ 7]) & 0xffffffff, 18)
            x[ 1] ^= rotl((x[ 0] + x[ 3]) & 0xffffffff, 7)
            x[ 2] ^= rotl((x[ 1] + x[ 0]) & 0xffffffff, 9)
            x[ 3] ^= rotl((x[ 2] + x[ 1]) & 0xffffffff, 13)
            x[ 0] ^= rotl((x[ 3] + x[ 2]) & 0xffffffff, 18)
            x[ 6] ^= rotl((x[ 5] + x[ 4]) & 0xffffffff, 7)
            x[ 7] ^= rotl((x[ 6] + x[ 5]) & 0xffffffff, 9)
            x[ 4] ^= rotl((x[ 7] + x[ 6]) & 0xffffffff, 13)
            x[ 5] ^= rotl((x[ 4] + x[ 7]) & 0xffffffff, 18)
            x[11] ^= rotl((x[10] + x[ 9]) & 0xffffffff, 7)
            x[ 8] ^= rotl((x[11] + x[10]) & 0xffffffff, 9)
            x[ 9] ^= rotl((x[ 8] + x[11]) & 0xffffffff, 13)
            x[10] ^= rotl((x[ 9] + x[ 8]) & 0xffffffff, 18)
            x[12] ^= rotl((x[15] + x[14]) & 0xffffffff, 7)
            x[13] ^= rotl((x[12] + x[15]) & 0xffffffff, 9)
            x[14] ^= rotl((x[13] + x[12]) & 0xffffffff, 13)
            x[15] ^= rotl((x[14] + x[13]) & 0xffffffff, 18)
        
        return x
    
    def blockmix(B, r):
        """scryptBlockMix"""
        X = list(B[-16:])
        Y = []
        
        for i in range(2 * r):
            for j in range(16):
                X[j] ^= B[i * 16 + j]
            X = salsa20_8(X)
            Y.extend(X)
        
        result = [0] * (32 * r)
        for i in range(r):
            result[i * 16:(i + 1) * 16] = Y[i * 32:(i + 1) * 16]
            result[(i + r) * 16:(i + r + 1) * 16] = Y[i * 32 + 16:(i + 1) * 32]
        
        return result
    
    def romix(B, N):
        """scryptROMix"""
        V = []
        X = list(B)
        
        for i in range(N):
            V.append(list(X))
            X = blockmix(X, r)
        
        for i in range(N):
            j = X[-16] % N
            for k in range(len(X)):
                X[k] ^= V[j][k]
            X = blockmix(X, r)
        
        return X
    
    # Convert password and salt to bytes if needed
    if isinstance(password, str):
        password = password.encode('utf-8')
    if isinstance(salt, str):
        salt = salt.encode('utf-8')
    
    # PBKDF2 to generate initial key
    B = hashlib.pbkdf2_hmac('sha256', password, salt, 1, p * 128 * r)
    
    # Convert to 32-bit integers
    result = []
    for i in range(p):
        block_start = i * 128 * r
        block = B[block_start:block_start + 128 * r]
        block_ints = []
        for j in range(0, len(block), 4):
            val = int.from_bytes(block[j:j+4], 'little')
            block_ints.append(val)
        
        # Apply ROMix
        mixed = romix(block_ints, N)
        
        # Convert back to bytes
        mixed_bytes = b''
        for val in mixed:
            mixed_bytes += val.to_bytes(4, 'little')
        
        result.append(mixed_bytes)
    
    # Final PBKDF2
    final_input = b''.join(result)
    return hashlib.pbkdf2_hmac('sha256', password, final_input, 1, dkLen)

# Read input
password = input().strip()
salt = input().strip()

# Generate scrypt key
key = scrypt(password, salt, N=16384, r=8, p=1, dkLen=32)

# Output as hex
print(key.hex())