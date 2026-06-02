import sys
from collections import Counter

# Read all input from stdin
text = sys.stdin.read().strip()

# Split into words
words = text.split()

# Count word frequencies
word_counts = Counter(words)

# Sort by frequency (descending) then alphabetically
sorted_words = sorted(word_counts.items(), key=lambda x: (-x[1], x[0]))

# Output in the required format
for word, count in sorted_words:
    print(f"{word}: {count}")