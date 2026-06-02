import hashlib

def hash_functions(item, num_hashes, filter_size):
    """Generate multiple hash values for an item"""
    hashes = []
    for i in range(num_hashes):
        # Create different hash functions by combining item with seed
        hash_input = f"{item}_{i}".encode('utf-8')
        hash_value = int(hashlib.md5(hash_input).hexdigest(), 16) % filter_size
        hashes.append(hash_value)
    return hashes

# Read input
filter_size = int(input().strip())
num_hash_functions = int(input().strip())
items_to_add = input().strip().split(',')
items_to_check = input().strip().split(',')

# Initialize bloom filter (bit array)
bloom_filter = [0] * filter_size

# Add items to bloom filter
for item in items_to_add:
    hash_values = hash_functions(item, num_hash_functions, filter_size)
    for hash_val in hash_values:
        bloom_filter[hash_val] = 1

# Check items
for item in items_to_check:
    hash_values = hash_functions(item, num_hash_functions, filter_size)
    all_bits_set = True
    for hash_val in hash_values:
        if bloom_filter[hash_val] == 0:
            all_bits_set = False
            break
    
    if all_bits_set:
        print("PROBABLY_IN")
    else:
        print("DEFINITELY_NOT_IN")