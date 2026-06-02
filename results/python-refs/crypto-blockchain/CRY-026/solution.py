import sys

# Read input
key = input().strip()
plaintext = input().strip()

# Convert to bytes
key_bytes = key.encode('utf-8')
plaintext_bytes = plaintext.encode('utf-8')

# XOR cipher with cyclic key
result = []
for i, byte in enumerate(plaintext_bytes):
    key_byte = key_bytes[i % len(key_bytes)]
    xor_result = byte ^ key_byte
    result.append(xor_result)

# Convert to hex
hex_output = ''.join(f'{byte:02x}' for byte in result)
print(hex_output)