import urllib.parse
import sys

encoded_string = input().strip()
decoded_string = urllib.parse.unquote(encoded_string)
print(decoded_string)