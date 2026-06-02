import hashlib
import sys

def sha512(data):
    return hashlib.sha512(data).digest()

def mod_inverse(a, m):
    if a < 0:
        a = (a % m + m) % m
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    return x % m

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def bytes_to_int(b):
    return int.from_bytes(b, 'little')

def int_to_bytes(x, length):
    return x.to_bytes(length, 'little')

# Ed25519 parameters
p = 2**255 - 19
d = -121665 * mod_inverse(121666, p) % p
q = 2**252 + 27742317777372353535851937790883648493
B = (15112221349535400772501151409588531511454012693041857206046113283949847762202, 
     46316835694926478169428394003475163141307993866256225615783033603165251855960)

def point_add(P1, P2):
    if P1 is None:
        return P2
    if P2 is None:
        return P1
    
    x1, y1 = P1
    x2, y2 = P2
    
    x3 = (x1*y2 + y1*x2) * mod_inverse(1 + d*x1*x2*y1*y2, p) % p
    y3 = (y1*y2 - x1*x2) * mod_inverse(1 - d*x1*x2*y1*y2, p) % p
    
    return (x3, y3)

def scalar_mult(k, P):
    if k == 0:
        return None
    if k == 1:
        return P
    
    result = None
    addend = P
    
    while k:
        if k & 1:
            result = point_add(result, addend)
        addend = point_add(addend, addend)
        k >>= 1
    
    return result

def point_compress(P):
    x, y = P
    return int_to_bytes(y | ((x & 1) << 255), 32)

def clamp_scalar(s):
    s_bytes = list(s)
    s_bytes[0] &= 248
    s_bytes[31] &= 127
    s_bytes[31] |= 64
    return bytes(s_bytes)

def sign_message(private_key_bytes, message):
    # Hash private key
    h = sha512(private_key_bytes)
    
    # Clamp the first 32 bytes to get scalar a
    a_bytes = clamp_scalar(h[:32])
    a = bytes_to_int(a_bytes) % q
    
    # Compute public key A = a * B
    A = scalar_mult(a, B)
    A_bytes = point_compress(A)
    
    # Compute r = H(h[32:64] || message)
    r_hash = sha512(h[32:] + message)
    r = bytes_to_int(r_hash) % q
    
    # Compute R = r * B
    R = scalar_mult(r, B)
    R_bytes = point_compress(R)
    
    # Compute k = H(R || A || message)
    k_hash = sha512(R_bytes + A_bytes + message)
    k = bytes_to_int(k_hash) % q
    
    # Compute S = (r + k * a) mod q
    S = (r + k * a) % q
    S_bytes = int_to_bytes(S, 32)
    
    # Return signature R || S
    return R_bytes + S_bytes

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

private_key_hex = lines[0]
message = lines[1]

# Convert hex private key to bytes
private_key_bytes = bytes.fromhex(private_key_hex)

# Sign the message
message_bytes = message.encode('utf-8')
signature = sign_message(private_key_bytes, message_bytes)

# Output signature as hex
print(signature.hex())