import sys, hashlib
data = sys.stdin.read().split('\n')
pwd = data[0].encode()
salt = data[1].encode()
key = hashlib.scrypt(pwd, salt=salt, n=16384, r=8, p=1, dklen=32)
print(key.hex())
