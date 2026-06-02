import sys

text = sys.stdin.read().strip()
hex_output = text.encode('utf-8').hex()
print(hex_output)