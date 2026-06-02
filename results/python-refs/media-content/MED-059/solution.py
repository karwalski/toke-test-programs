import base64
import sys

text = sys.stdin.read().strip()
encoded = base64.b64encode(text.encode('utf-8')).decode('utf-8')
print(encoded)