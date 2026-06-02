def compute_lps(pattern):
    """Compute the Longest Proper Prefix which is also Suffix array"""
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1
    
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text, pattern):
    """KMP algorithm to find all occurrences of pattern in text"""
    n = len(text)
    m = len(pattern)
    
    if m == 0:
        return [], 0
    
    lps = compute_lps(pattern)
    positions = []
    comparisons = 0
    
    i = 0  # index for text
    j = 0  # index for pattern
    
    while i < n:
        comparisons += 1
        if text[i] == pattern[j]:
            i += 1
            j += 1
        
        if j == m:
            positions.append(i - j)
            j = lps[j - 1]
        elif i < n and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    
    return positions, comparisons

# Read input
pattern = input().strip()
text = input().strip()

# Find all occurrences
positions, comparisons = kmp_search(text, pattern)

# Output results
if positions:
    print("Found at positions:", " ".join(map(str, positions)))
else:
    print("NOT FOUND")

print(f"Comparisons: {comparisons}")