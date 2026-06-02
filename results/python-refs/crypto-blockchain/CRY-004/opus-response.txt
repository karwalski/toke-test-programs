import hmac
import hashlib
import sys

data = sys.stdin.read().split('\n')
key = data[0]
message = data[1] if len(data) > 1 else ''

hmac_hash = hmac.new(key.encode('utf-8'), message.encode('utf-8'), hashlib.sha256)
print(hmac_hash.hexdigest())