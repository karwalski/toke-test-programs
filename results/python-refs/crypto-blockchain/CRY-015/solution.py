import hashlib

text = input()
hash_object = hashlib.sha3_256(text.encode('utf-8'))
print(hash_object.hexdigest())