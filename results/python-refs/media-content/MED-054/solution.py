import sys
from collections import defaultdict

# Read input and split into words
words = input().strip().split()

# Group words by their sorted character signature
anagram_groups = defaultdict(list)
for word in words:
    signature = ''.join(sorted(word))
    anagram_groups[signature].append(word)

# Prepare output groups
output_groups = []
for group in anagram_groups.values():
    group.sort()  # Sort words within each group
    output_groups.append(group)

# Sort groups by their first word
output_groups.sort(key=lambda x: x[0])

# Print output
for group in output_groups:
    print(' '.join(group))