import sys
from collections import Counter

text = sys.stdin.read().strip()
char_count = Counter(text)

# Sort by frequency descending, then by character ascending
sorted_chars = sorted(char_count.items(), key=lambda x: (-x[1], x[0]))

for char, count in sorted_chars:
    print(f"{char}: {count}")