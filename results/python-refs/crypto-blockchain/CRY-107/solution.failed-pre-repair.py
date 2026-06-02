import hashlib

# Read the lowercase address from stdin
address = input().strip()

# Calculate Keccak-256 hash of the address
# Since we don't have a direct Keccak implementation, we'll use SHA-3 which is available in hashlib
hash_obj = hashlib.sha3_256(address.encode('utf-8'))
hash_hex = hash_obj.hexdigest()

# Apply EIP-55 checksum rules
checksummed = ""
for i, char in enumerate(address):
    if char.isdigit():
        checksummed += char
    else:
        # If the corresponding hex digit in the hash is >= 8, capitalize
        if int(hash_hex[i], 16) >= 8:
            checksummed += char.upper()
        else:
            checksummed += char

# Output with 0x prefix
print(f"0x{checksummed}")