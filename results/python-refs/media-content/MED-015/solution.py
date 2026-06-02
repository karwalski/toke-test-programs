import sys
from collections import Counter

# Read all input from stdin
text = sys.stdin.read().strip()

# Split into words and count frequencies
words = text.split()
word_counts = Counter(words)

# Get the most common words, limited to top 10
most_common = word_counts.most_common(10)

# Format output as 'word(N)' and join with spaces
output = ' '.join(f"{word}({count})" for word, count in most_common)

print(output)