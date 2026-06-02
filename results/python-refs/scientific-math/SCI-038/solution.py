def build_suffix_array(text):
    n = len(text)
    suffixes = [(text[i:], i) for i in range(n)]
    suffixes.sort()
    return [suffix[1] for suffix in suffixes]

def find_pattern_occurrences(text, pattern, suffix_array):
    occurrences = []
    pattern_len = len(pattern)
    
    for start_pos in suffix_array:
        if start_pos + pattern_len <= len(text):
            if text[start_pos:start_pos + pattern_len] == pattern:
                occurrences.append(start_pos)
    
    return sorted(occurrences)

# Read input
text = input().strip()
pattern = input().strip()

# Build suffix array
suffix_array = build_suffix_array(text)

# Find pattern occurrences
occurrences = find_pattern_occurrences(text, pattern, suffix_array)

# Output results
print("Suffix array:", " ".join(map(str, suffix_array)))
if occurrences:
    print("Pattern found at:", " ".join(map(str, occurrences)))
else:
    print("NOT FOUND")