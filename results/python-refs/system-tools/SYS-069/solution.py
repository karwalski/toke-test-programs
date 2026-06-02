import sys
from collections import Counter
import re

# Read input
lines = sys.stdin.read().strip().split('\n')
top_n = int(lines[0])
text_lines = lines[1:]

# Join all text lines
full_text = '\n'.join(text_lines)

# Count lines
line_count = len(text_lines)

# Count characters (including newlines)
char_count = len(full_text)

# Count words
words = []
for line in text_lines:
    words.extend(line.split())
word_count = len(words)

# Calculate average line length
if line_count > 0:
    avg_line_length = sum(len(line) for line in text_lines) / line_count
else:
    avg_line_length = 0.0

# Get top N words
word_counter = Counter(words)
top_words = word_counter.most_common(top_n)

# Format top words output
top_words_str = ','.join(f"{word}:{count}" for word, count in top_words)

# Output results
print(f"Lines: {line_count}, Words: {word_count}, Chars: {char_count}, Avg line: {avg_line_length}, Top words: {top_words_str}")