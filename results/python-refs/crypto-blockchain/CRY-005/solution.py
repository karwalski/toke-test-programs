import sys
import base64

text = sys.stdin.read().strip()
encoded = base64.b64encode(text.encode('utf-8')).decode('ascii')
print(encoded)