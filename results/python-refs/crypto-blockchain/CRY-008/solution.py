import sys

hex_string = sys.stdin.read().strip()
decoded = bytes.fromhex(hex_string).decode('utf-8')
print(decoded)