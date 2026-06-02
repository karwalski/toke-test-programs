import sys
from collections import Counter

# Read input from stdin
text = sys.stdin.read().strip()

# Split text into words
words = text.split()

# Extract bigrams
bigrams = []
for i in range(len(words) - 1):
    bigram = f"{words[i]} {words[i+1]}"
    bigrams.append(bigram)

# Count frequencies
counts = Counter(bigrams)

# Sort by count descending
sorted_bigrams = sorted(counts.items(), key=lambda x: x[1], reverse=True)

# Output in required format
for bigram, count in sorted_bigrams:
    print(f'"{bigram}": {count}')