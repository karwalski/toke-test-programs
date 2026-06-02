from Crypto.Cipher import AES
import sys

# Read input
key_hex = input().strip()
iv_hex = input().strip()
plaintext = input().strip()

# Convert hex strings to bytes
key = bytes.fromhex(key_hex)
iv = bytes.fromhex(iv_hex)

# Create AES cipher in CBC mode
cipher = AES.new(key, AES.MODE_CBC, iv)

# Pad plaintext to multiple of 16 bytes (PKCS7 padding)
def pkcs7_pad(data, block_size=16):
    padding_len = block_size - (len(data) % block_size)
    padding = bytes([padding_len] * padding_len)
    return data + padding

plaintext_bytes = plaintext.encode('utf-8')
padded_plaintext = pkcs7_pad(plaintext_bytes)

# Encrypt
ciphertext = cipher.encrypt(padded_plaintext)

# Output as hex
print(ciphertext.hex())