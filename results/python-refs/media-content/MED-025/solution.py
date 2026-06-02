import sys
from collections import Counter

# Read all input from stdin
text = sys.stdin.read().strip()

# Split into words
words = text.split()

# Extract trigrams
trigrams = []
for i in range(len(words) - 2):
    trigram = f'"{words[i]} {words[i+1]} {words[i+2]}"'
    trigrams.append(trigram)

# Count frequencies
counts = Counter(trigrams)

# Sort by count descending, then by trigram for stability
sorted_trigrams = sorted(counts.items(), key=lambda x: (-x[1], x[0]))

# Output only the most frequent trigram
if sorted_trigrams:
    trigram, count = sorted_trigrams[0]
    print(f"{trigram}: {count}")