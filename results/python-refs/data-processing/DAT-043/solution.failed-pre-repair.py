import sys
from heapq import heappush, heappop
from collections import Counter

class Node:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right
    
    def __lt__(self, other):
        if self.freq != other.freq:
            return self.freq < other.freq
        # For tie-breaking, prefer leaf nodes (with chars) over internal nodes
        if self.char is None and other.char is not None:
            return False
        if self.char is not None and other.char is None:
            return True
        if self.char is not None and other.char is not None:
            return self.char < other.char
        return False

def build_huffman_tree(text):
    # Count frequencies
    freq_counter = Counter(text)
    
    # Handle single character case
    if len(freq_counter) == 1:
        char = list(freq_counter.keys())[0]
        root = Node(char, freq_counter[char])
        return root, {char: '0'}
    
    # Create heap with leaf nodes
    heap = []
    for char, freq in freq_counter.items():
        heappush(heap, Node(char, freq))
    
    # Build tree
    while len(heap) > 1:
        left = heappop(heap)
        right = heappop(heap)
        merged = Node(freq=left.freq + right.freq, left=left, right=right)
        heappush(heap, merged)
    
    root = heap[0]
    
    # Generate codes
    codes = {}
    
    def generate_codes(node, code=''):
        if node.char is not None:  # Leaf node
            codes[node.char] = code if code else '0'
        else:
            if node.left:
                generate_codes(node.left, code + '0')
            if node.right:
                generate_codes(node.right, code + '1')
    
    generate_codes(root)
    return root, codes

def main():
    text = input().strip()
    
    if not text:
        return
    
    root, codes = build_huffman_tree(text)
    
    # Sort codes by length then by character
    sorted_codes = sorted(codes.items(), key=lambda x: (len(x[1]), x[0]))
    
    # Print code table
    for char, code in sorted_codes:
        print(f"{char}: {code}")
    
    # Encode text
    encoded = ''.join(codes[char] for char in text)
    print(f"Encoded: {encoded}")
    
    # Calculate compression ratio
    original_bits = len(text) * 8
    compressed_bits = len(encoded)
    ratio = compressed_bits / original_bits
    print(f"Ratio: {ratio:.2f}")

if __name__ == "__main__":
    main()