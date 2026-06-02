import sys
import re

# Read all input text
text = sys.stdin.read().strip()

# Extract words (alphabetic characters only)
words = re.findall(r'[a-zA-Z]+', text)

if not words:
    sys.exit()

# Find maximum length
max_length = max(len(word) for word in words)

# Find all words with maximum length
longest_words = [word for word in words if len(word) == max_length]

# Remove duplicates and sort alphabetically
unique_longest = sorted(set(longest_words))

# Output one word per line
for word in unique_longest:
    print(word)