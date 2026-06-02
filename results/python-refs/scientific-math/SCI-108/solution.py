import hashlib
import math
import sys

class BloomFilter:
    def __init__(self, capacity, false_positive_rate):
        self.capacity = capacity
        self.false_positive_rate = false_positive_rate
        
        # Calculate optimal number of bits and hash functions
        self.num_bits = math.ceil(-capacity * math.log(false_positive_rate) / (math.log(2) ** 2))
        self.num_hashes = math.ceil(self.num_bits / capacity * math.log(2))
        
        # Initialize bit array
        self.bit_array = [False] * self.num_bits
        self.items_added = 0
    
    def _hash(self, item, seed):
        """Generate hash using sha256 with seed"""
        hasher = hashlib.sha256()
        hasher.update(str(seed).encode('utf-8'))
        hasher.update(item.encode('utf-8'))
        return int(hasher.hexdigest(), 16) % self.num_bits
    
    def add(self, item):
        """Add an item to the bloom filter"""
        for i in range(self.num_hashes):
            bit_index = self._hash(item, i)
            self.bit_array[bit_index] = True
        self.items_added += 1
    
    def contains(self, item):
        """Check if item might be in the set"""
        for i in range(self.num_hashes):
            bit_index = self._hash(item, i)
            if not self.bit_array[bit_index]:
                return False
        return True
    
    def stats(self):
        """Return statistics about the bloom filter"""
        bits_set = sum(self.bit_array)
        fill_percentage = (bits_set / self.num_bits) * 100
        return f"bits={self.num_bits} k={self.num_hashes} fill={fill_percentage:.2f}%"

def main():
    # Read first line with capacity and false positive rate
    first_line = input().strip()
    capacity, false_positive_rate = first_line.split()
    capacity = int(capacity)
    false_positive_rate = float(false_positive_rate)
    
    bloom = BloomFilter(capacity, false_positive_rate)
    
    # Process commands
    try:
        while True:
            line = input().strip()
            if not line:
                break
                
            parts = line.split(' ', 1)
            command = parts[0]
            
            if command == "ADD":
                item = parts[1]
                bloom.add(item)
            elif command == "CONTAINS":
                item = parts[1]
                if bloom.contains(item):
                    print("PROBABLY_IN")
                else:
                    print("NOT_IN")
            elif command == "STATS":
                print(bloom.stats())
                
    except EOFError:
        pass

if __name__ == "__main__":
    main()