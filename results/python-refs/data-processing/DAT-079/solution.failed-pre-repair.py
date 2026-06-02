import sys
from collections import defaultdict

# Read input
lines = sys.stdin.read().strip().split('\n')
window_size = int(lines[0])
text = lines[1]

# Tokenize text into words
words = text.split()

# Build co-occurrence matrix
cooccurrence = defaultdict(int)

# For each word position, look at words within the window
for i in range(len(words)):
    for j in range(max(0, i - window_size), min(len(words), i + window_size + 1)):
        if i != j:  # Don't count self-occurrences
            word1 = words[i]
            word2 = words[j]
            # Create ordered pair to avoid duplicates (word1, word2) same as (word2, word1)
            pair = tuple(sorted([word1, word2]))
            cooccurrence[pair] += 1

# Sort by count (descending) then by word pairs for consistent output
sorted_pairs = sorted(cooccurrence.items(), key=lambda x: (-x[1], x[0]))

# Output CSV format
print("word1,word2,count")
for (word1, word2), count in sorted_pairs:
    print(f"{word1},{word2},{count}")