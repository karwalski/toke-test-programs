import hashlib
import sys

class BloomFilter:
    def __init__(self, size, hash_count):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = [False] * size
    
    def _hash(self, item, seed):
        """Generate hash for item with given seed"""
        hash_input = f"{item}{seed}".encode('utf-8')
        return int(hashlib.md5(hash_input).hexdigest(), 16) % self.size
    
    def add(self, item):
        """Add item to the bloom filter"""
        for i in range(self.hash_count):
            index = self._hash(item, i)
            self.bit_array[index] = True
    
    def check(self, item):
        """Check if item might be in the set"""
        for i in range(self.hash_count):
            index = self._hash(item, i)
            if not self.bit_array[index]:
                return False
        return True

# Read filter configuration
line = input().strip()
size, hash_count = map(int, line.split())

# Initialize bloom filter
bloom_filter = BloomFilter(size, hash_count)

# Process commands
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    parts = line.split(' ', 1)
    command = parts[0]
    item = parts[1]
    
    if command == 'add':
        bloom_filter.add(item)
        print(f"Added: {item}")
    elif command == 'check':
        if bloom_filter.check(item):
            print(f"Possibly in set: {item}")
        else:
            print(f"Definitely not in set: {item}")