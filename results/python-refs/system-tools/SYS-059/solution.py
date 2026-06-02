import base64
import sys

lines = sys.stdin.read().strip().split('\n')
mode = lines[0]
data = '\n'.join(lines[1:])

if mode == 'encode':
    result = base64.b64encode(data.encode()).decode()
elif mode == 'decode':
    result = base64.b64decode(data.encode()).decode()
elif mode == 'encode-url':
    result = base64.urlsafe_b64encode(data.encode()).decode()
elif mode == 'decode-url':
    result = base64.urlsafe_b64decode(data.encode()).decode()

print(result)