def rabin_karp(pattern, text, base, mod):
    n = len(text)
    m = len(pattern)
    
    if m > n:
        return [], 0, 0
    
    # Calculate base^(m-1) % mod
    h = 1
    for i in range(m - 1):
        h = (h * base) % mod
    
    # Calculate hash of pattern and first window of text
    pattern_hash = 0
    text_hash = 0
    
    for i in range(m):
        pattern_hash = (pattern_hash * base + ord(pattern[i])) % mod
        text_hash = (text_hash * base + ord(text[i])) % mod
    
    positions = []
    spurious_hits = 0
    comparisons = 0
    
    # Check first window
    if pattern_hash == text_hash:
        comparisons += 1
        if text[0:m] == pattern:
            positions.append(0)
        else:
            spurious_hits += 1
    
    # Roll the hash over the text
    for i in range(1, n - m + 1):
        # Remove leading character and add trailing character
        text_hash = (text_hash - ord(text[i - 1]) * h) % mod
        text_hash = (text_hash * base + ord(text[i + m - 1])) % mod
        
        # Make sure hash is positive
        text_hash = (text_hash + mod) % mod
        
        # Check if hashes match
        if pattern_hash == text_hash:
            comparisons += 1
            if text[i:i + m] == pattern:
                positions.append(i)
            else:
                spurious_hits += 1
    
    return positions, spurious_hits, comparisons

# Read input
pattern = input().strip()
text = input().strip()
base_mod = input().strip().split()
base = int(base_mod[0])
mod = int(base_mod[1])

# Find occurrences
positions, spurious_hits, comparisons = rabin_karp(pattern, text, base, mod)

# Output results
if positions:
    print("Found at positions:", " ".join(map(str, positions)))
else:
    print("Found at positions:")
print(f"Spurious hits: {spurious_hits}")
print(f"Comparisons: {comparisons}")