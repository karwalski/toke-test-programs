import urllib.parse
import sys

input_text = sys.stdin.read().strip()
encoded_text = urllib.parse.quote(input_text)
print(encoded_text)