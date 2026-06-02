import sys
from collections import Counter
import heapq

def main():
    text = sys.stdin.read()
    if text.endswith('\n'):
        text = text[:-1]
    if not text:
        return
    
    freq = Counter(text)
    
    # Build Huffman tree, get code lengths
    # Use heap with tiebreak: internal nodes before leaves, then by char
    # Node: (freq, is_leaf_flag, tiebreak, payload)
    # payload is either char (leaf) or list of (char, depth-add) 
    
    if len(freq) == 1:
        ch = list(freq.keys())[0]
        lengths = {ch: 1}
    else:
        # Each entry: [freq, is_leaf(0=internal,1=leaf), char_for_leaf_or_'', counter, chars_list]
        heap = []
        counter = 0
        for ch in sorted(freq.keys()):
            heapq.heappush(heap, (freq[ch], 1, ch, counter, [ch]))
            counter += 1
        
        # Track depth for each char
        depths = {ch: 0 for ch in freq}
        
        while len(heap) > 1:
            a = heapq.heappop(heap)
            b = heapq.heappop(heap)
            for ch in a[4]:
                depths[ch] += 1
            for ch in b[4]:
                depths[ch] += 1
            # Merged is internal (is_leaf=0, comes first in tiebreak)
            merged_chars = a[4] + b[4]
            # For tiebreak among internals, use first char
            heapq.heappush(heap, (a[0]+b[0], 0, '', counter, merged_chars))
            counter += 1
        
        lengths = depths
    
    # Canonical Huffman coding
    # Sort by (length, char)
    sorted_chars = sorted(lengths.items(), key=lambda x: (x[1], x[0]))
    
    codes = {}
    code = 0
    prev_len = 0
    for ch, length in sorted_chars:
        if prev_len == 0:
            code = 0
        else:
            code = (code + 1) << (length - prev_len)
        codes[ch] = format(code, '0{}b'.format(length)) if length > 0 else '0'
        prev_len = length
    
    # Special case: single char
    if len(freq) == 1:
        ch = list(freq.keys())[0]
        codes[ch] = '0'
    
    # Output code table sorted by (code length, char)
    output_lines = []
    for ch, length in sorted_chars:
        output_lines.append(f"{ch}: {codes[ch]}")
    
    encoded = ''.join(codes[ch] for ch in text)
    output_lines.append(f"Encoded: {encoded}")
    
    ratio = len(encoded) / (len(text) * 8)
    output_lines.append(f"Ratio: {ratio:.2f}")
    
    print('\n'.join(output_lines))

main()