import sys
import re

# Read all input from stdin
text = sys.stdin.read().strip()

# Split into sentences using regex to handle periods, exclamation marks, question marks
sentences = re.split(r'[.!?]+', text)

# Filter out empty sentences
sentences = [s.strip() for s in sentences if s.strip()]

# Count words in each sentence
word_counts = []
for sentence in sentences:
    words = sentence.split()
    word_counts.append(len(words))

# Calculate min, max, and average
min_words = min(word_counts)
max_words = max(word_counts)
avg_words = sum(word_counts) / len(word_counts)

# Output in required format
print(f"min: {min_words}")
print(f"max: {max_words}")
print(f"avg: {avg_words:.1f}")