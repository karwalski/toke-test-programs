import secrets

# Generate a cryptographically random UUID v4
# UUID v4 format: xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx
# where y is one of 8, 9, a, b

# Generate 16 random bytes
random_bytes = secrets.token_bytes(16)

# Convert to hex string without dashes
hex_string = random_bytes.hex()

# Set version bits (4 in the 13th character position)
# Replace character at position 12 (0-indexed) with '4'
hex_list = list(hex_string)
hex_list[12] = '4'

# Set variant bits (first two bits of the 17th character should be 10)
# This means the 17th character (position 16) should be 8, 9, a, or b
variant_char = hex_list[16]
# Map any hex digit to 8, 9, a, b based on last 2 bits
variant_map = {'0': '8', '1': '9', '2': 'a', '3': 'b', 
               '4': '8', '5': '9', '6': 'a', '7': 'b',
               '8': '8', '9': '9', 'a': 'a', 'b': 'b',
               'c': '8', 'd': '9', 'e': 'a', 'f': 'b'}
hex_list[16] = variant_map[variant_char]

# Join back to string
hex_string = ''.join(hex_list)

# Format with dashes: xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx
uuid = f"{hex_string[0:8]}-{hex_string[8:12]}-{hex_string[12:16]}-{hex_string[16:20]}-{hex_string[20:32]}"

print(uuid)