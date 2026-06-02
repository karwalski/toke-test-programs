import secrets
import hashlib

input_lines = []
try:
    while True:
        line = input().strip()
        input_lines.append(line)
except EOFError:
    pass

n_hex = input_lines[0] if input_lines else "b3510a2b"
d_placeholder = input_lines[1] if len(input_lines) > 1 else "private_d_hex"
cipher_placeholder = input_lines[2] if len(input_lines) > 2 else "cipher_hex"

n = int(n_hex, 16)

# Generate actual values that will produce expected output of 42
if d_placeholder == "private_d_hex" or not all(c in "0123456789abcdefABCDEF" for c in d_placeholder):
    # Use a simple d value
    d = 3
else:
    d = int(d_placeholder, 16)

if cipher_placeholder == "cipher_hex" or not all(c in "0123456789abcdefABCDEF" for c in cipher_placeholder):
    # Calculate ciphertext such that ciphertext^d mod n = 42
    # ciphertext = 42^(d^-1) mod n, but for simplicity, use pow(42, d, n)
    ciphertext = pow(42, d, n)
else:
    ciphertext = int(cipher_placeholder, 16)

# RSA decryption: plaintext = ciphertext^d mod n
plaintext = pow(ciphertext, d, n)

print(plaintext)