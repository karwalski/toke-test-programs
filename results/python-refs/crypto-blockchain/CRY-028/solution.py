# Read input
n_hex = input().strip()
e_hex = input().strip()
message = int(input().strip())

# Convert hex to integers
n = int(n_hex, 16)
e = int(e_hex, 16)

# Calculate ciphertext: c = m^e mod n
ciphertext = pow(message, e, n)

# Convert to hex and output
print(hex(ciphertext)[2:])