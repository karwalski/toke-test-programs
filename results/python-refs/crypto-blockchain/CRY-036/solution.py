import secrets

n = int(input())
random_bytes = secrets.token_bytes(n)
hex_string = random_bytes.hex()
print(hex_string)