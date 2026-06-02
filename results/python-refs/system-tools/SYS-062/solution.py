import sys
import hashlib

# Read the algorithm from the first line
algorithm = sys.stdin.readline().strip()

# Read the remaining data (binary safe)
data = sys.stdin.read().encode('utf-8')

# Create the appropriate hash object
if algorithm == 'md5':
    hash_obj = hashlib.md5()
elif algorithm == 'sha1':
    hash_obj = hashlib.sha1()
elif algorithm == 'sha256':
    hash_obj = hashlib.sha256()
elif algorithm == 'sha512':
    hash_obj = hashlib.sha512()
else:
    raise ValueError(f"Unsupported algorithm: {algorithm}")

# Update the hash with the data
hash_obj.update(data)

# Output the hex-encoded hash
print(hash_obj.hexdigest())