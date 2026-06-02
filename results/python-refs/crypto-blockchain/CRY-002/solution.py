import hashlib
import sys

text = input().strip()
hash_object = hashlib.sha512(text.encode('utf-8'))
print(hash_object.hexdigest())