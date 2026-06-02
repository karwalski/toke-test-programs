import heapq
import sys

class Node:
    def __init__(self, char, freq, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right
    
    def __lt__(self, other):
        if self.freq != other.freq:
            return self.freq < other.freq
        # For tie-breaking, prioritize leaf nodes over internal nodes
        if self.char is None and other.char is not None:
            return False
        if self.char is not None and other.char is None:
            return True
        # If both are leaf nodes, compare by character
        if self.char is not None and other.char is not None:
            return self.char < other.char
        # Both are internal nodes
        return False

def build_huffman_tree(frequencies):
    if len(frequencies) == 1:
        # Special case: only one symbol
        char = list(frequencies.keys())[0]
        root = Node(char, frequencies[char])
        return root
    
    heap = []
    for char, freq in frequencies.items():
        heapq.heappush(heap, Node(char, freq))
    
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq, left, right)
        heapq.heappush(heap, merged)
    
    return heap[0]

def generate_codes(root):
    if root is None:
        return {}
    
    codes = {}
    
    def traverse(node, code):
        if node.char is not None:  # Leaf node
            codes[node.char] = code if code else "0"  # Handle single character case
        else:
            if node.left:
                traverse(node.left, code + "0")
            if node.right:
                traverse(node.right, code + "1")
    
    traverse(root, "")
    return codes

def decode_message(root, bitstring):
    if not bitstring:
        return ""
    
    if root.char is not None:  # Single character tree
        return root.char * len(bitstring)
    
    result = []
    current = root
    
    for bit in bitstring:
        if bit == "0":
            current = current.left
        else:
            current = current.right
        
        if current.char is not None:  # Reached leaf
            result.append(current.char)
            current = root
    
    return "".join(result)

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    mode = lines[0]
    
    # Parse frequencies
    frequencies = {}
    i = 1
    while i < len(lines) and lines[i] != "---":
        parts = lines[i].split()
        char = parts[0]
        freq = int(parts[1])
        frequencies[char] = freq
        i += 1
    
    # Build Huffman tree
    root = build_huffman_tree(frequencies)
    codes = generate_codes(root)
    
    if mode == "build":
        # Sort by code length, then by code value, then by character
        sorted_items = sorted(codes.items(), key=lambda x: (len(x[1]), x[1], x[0]))
        for char, code in sorted_items:
            print(f"{char} {code}")
    
    elif mode == "encode":
        message = lines[i + 1]
        encoded = "".join(codes[char] for char in message)
        print(encoded)
    
    elif mode == "decode":
        bitstring = lines[i + 1]
        decoded = decode_message(root, bitstring)
        print(decoded)

if __name__ == "__main__":
    main()