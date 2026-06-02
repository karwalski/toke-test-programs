import sys
import urllib.parse

mode = input().strip()
text = input()

if mode == "encode":
    result = urllib.parse.quote(text)
elif mode == "decode":
    result = urllib.parse.unquote(text)

print(result)