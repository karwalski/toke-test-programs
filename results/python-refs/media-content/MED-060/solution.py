import base64
import sys

encoded_string = sys.stdin.read().strip()
decoded_bytes = base64.b64decode(encoded_string)
decoded_text = decoded_bytes.decode('utf-8')
print(decoded_text)