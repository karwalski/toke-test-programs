from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import sys

# Read input from stdin
key_hex = input().strip()
iv_hex = input().strip()
ciphertext_hex = input().strip()

# Convert hex strings to bytes
key = bytes.fromhex(key_hex)
iv = bytes.fromhex(iv_hex)
ciphertext = bytes.fromhex(ciphertext_hex)

# Create AES cipher in CBC mode
cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
decryptor = cipher.decryptor()

# Decrypt the ciphertext
decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()

# Remove PKCS7 padding
padding_length = decrypted_padded[-1]
decrypted = decrypted_padded[:-padding_length]

# Convert to string and print
plaintext = decrypted.decode('utf-8')
print(plaintext)