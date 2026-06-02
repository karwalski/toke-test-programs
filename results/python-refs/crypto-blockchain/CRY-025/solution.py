import sys, struct

def rotl32(x, n):
    return ((x << n) & 0xffffffff) | (x >> (32 - n))

def quarter_round(s, a, b, c, d):
    s[a] = (s[a] + s[b]) & 0xffffffff; s[d] ^= s[a]; s[d] = rotl32(s[d], 16)
    s[c] = (s[c] + s[d]) & 0xffffffff; s[b] ^= s[c]; s[b] = rotl32(s[b], 12)
    s[a] = (s[a] + s[b]) & 0xffffffff; s[d] ^= s[a]; s[d] = rotl32(s[d], 8)
    s[c] = (s[c] + s[d]) & 0xffffffff; s[b] ^= s[c]; s[b] = rotl32(s[b], 7)

def chacha20_block(key, counter, nonce):
    constants = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574]
    key_words = list(struct.unpack('<8I', key))
    nonce_words = list(struct.unpack('<3I', nonce))
    state = constants + key_words + [counter] + nonce_words
    working = state[:]
    for _ in range(10):
        quarter_round(working, 0, 4, 8, 12)
        quarter_round(working, 1, 5, 9, 13)
        quarter_round(working, 2, 6, 10, 14)
        quarter_round(working, 3, 7, 11, 15)
        quarter_round(working, 0, 5, 10, 15)
        quarter_round(working, 1, 6, 11, 12)
        quarter_round(working, 2, 7, 8, 13)
        quarter_round(working, 3, 4, 9, 14)
    out = [(working[i] + state[i]) & 0xffffffff for i in range(16)]
    return struct.pack('<16I', *out)

def chacha20_encrypt(key, counter, nonce, plaintext):
    out = bytearray()
    for i in range(0, len(plaintext), 64):
        block = chacha20_block(key, counter + i // 64, nonce)
        chunk = plaintext[i:i+64]
        out.extend(b ^ k for b, k in zip(chunk, block))
    return bytes(out)

def poly1305_key_gen(key, nonce):
    return chacha20_block(key, 0, nonce)[:32]

def poly1305_mac(msg, key):
    r = int.from_bytes(key[:16], 'little')
    r &= 0x0ffffffc0ffffffc0ffffffc0fffffff
    s = int.from_bytes(key[16:32], 'little')
    p = (1 << 130) - 5
    acc = 0
    for i in range(0, len(msg), 16):
        chunk = msg[i:i+16]
        n = int.from_bytes(chunk + b'\x01', 'little') if len(chunk) == 16 else int.from_bytes(chunk + b'\x01' + b'\x00' * (15 - len(chunk)), 'little')
        acc = (acc + n) % p
        acc = (acc * r) % p
    acc = (acc + s) & ((1 << 128) - 1)
    return acc.to_bytes(16, 'little')

def pad16(x):
    if len(x) % 16 == 0:
        return b''
    return b'\x00' * (16 - len(x) % 16)

def chacha20_poly1305_encrypt(key, nonce, plaintext, aad=b''):
    otk = poly1305_key_gen(key, nonce)
    ciphertext = chacha20_encrypt(key, 1, nonce, plaintext)
    mac_data = aad + pad16(aad) + ciphertext + pad16(ciphertext)
    mac_data += struct.pack('<Q', len(aad)) + struct.pack('<Q', len(ciphertext))
    tag = poly1305_mac(mac_data, otk)
    return ciphertext + tag

def main():
    data = sys.stdin.read().split('\n')
    key = bytes.fromhex(data[0].strip())
    nonce = bytes.fromhex(data[1].strip())
    plaintext = '\n'.join(data[2:])
    if plaintext.endswith('\n'):
        plaintext = plaintext[:-1]
    pt_bytes = plaintext.encode('utf-8')
    result = chacha20_poly1305_encrypt(key, nonce, pt_bytes)
    print(result.hex())

main()
