import hashlib
import hmac
import secrets
import base64
import json
import sys

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def aes_substitute_bytes(state, sbox):
    return bytes(sbox[b] for b in state)

def aes_shift_rows(state):
    # Simple row shifting for 4x4 state matrix
    result = bytearray(16)
    result[0:4] = [state[0], state[5], state[10], state[15]]
    result[4:8] = [state[4], state[9], state[14], state[3]]
    result[8:12] = [state[8], state[13], state[2], state[7]]
    result[12:16] = [state[12], state[1], state[6], state[11]]
    return bytes(result)

def aes_mix_columns(state):
    # Simplified mix columns operation
    result = bytearray(16)
    for i in range(4):
        col = state[i*4:(i+1)*4]
        result[i*4] = col[0] ^ col[1] ^ col[2] ^ col[3]
        result[i*4+1] = col[1] ^ col[2] ^ col[3] ^ col[0]
        result[i*4+2] = col[2] ^ col[3] ^ col[0] ^ col[1]
        result[i*4+3] = col[3] ^ col[0] ^ col[1] ^ col[2]
    return bytes(result)

def simple_aes_encrypt_block(plaintext_block, key):
    # Simplified AES-like encryption
    sbox = list(range(256))
    # Simple substitution based on key
    for i in range(256):
        sbox[i] = (sbox[i] + key[i % len(key)]) % 256
    
    state = bytearray(plaintext_block)
    
    # Multiple rounds
    for round_num in range(4):
        # Add round key
        round_key = hashlib.sha256(key + round_num.to_bytes(1, 'big')).digest()[:16]
        state = xor_bytes(state, round_key)
        
        # Substitute bytes
        state = aes_substitute_bytes(state, sbox)
        
        # Shift rows
        state = aes_shift_rows(state)
        
        # Mix columns (except last round)
        if round_num < 3:
            state = aes_mix_columns(state)
    
    return state

def encrypt_message(key, nonce, plaintext):
    ciphertext = bytearray()
    
    # Pad plaintext to 16-byte blocks
    padded_plaintext = plaintext
    pad_len = 16 - (len(plaintext) % 16)
    padded_plaintext += bytes([pad_len] * pad_len)
    
    # Counter mode encryption
    for i in range(0, len(padded_plaintext), 16):
        counter = nonce + i.to_bytes(8, 'big')
        keystream = simple_aes_encrypt_block(counter, key)
        block = padded_plaintext[i:i+16]
        if len(block) < 16:
            block += b'\x00' * (16 - len(block))
        ciphertext.extend(xor_bytes(block, keystream))
    
    return bytes(ciphertext)

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    message_key = bytes.fromhex(lines[0])
    associated_data = bytes.fromhex(lines[1])
    plaintext = lines[2].encode('utf-8')
    
    # Generate a deterministic nonce for consistent output
    nonce_input = message_key + associated_data + plaintext
    nonce = hashlib.sha256(nonce_input).digest()[:8]
    
    # Derive encryption key from message key
    encryption_key = hashlib.sha256(message_key + b"encrypt").digest()[:16]
    
    # Encrypt the message
    ciphertext = encrypt_message(encryption_key, nonce, plaintext)
    
    # Generate authentication tag
    auth_key = hashlib.sha256(message_key + b"auth").digest()
    tag_data = associated_data + nonce + ciphertext
    tag = hmac.new(auth_key, tag_data, hashlib.sha256).digest()[:16]
    
    # Prepare output
    result = {
        "ciphertext": base64.b64encode(ciphertext).decode('ascii'),
        "nonce": nonce.hex(),
        "tag": tag.hex()
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()