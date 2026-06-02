import sys

# Read the pattern from the first line
pattern = input().strip()

# Read all dictionary words
words = []
for line in sys.stdin:
    word = line.strip()
    if word:  # Skip empty lines
        words.append(word)

# Find matching words
matches = []
for word in words:
    # Check if word length matches pattern length
    if len(word) == len(pattern):
        # Check if word matches pattern
        match = True
        for i in range(len(pattern)):
            if pattern[i] != '?' and pattern[i] != word[i]:
                match = False
                break
        if match:
            matches.append(word)

# Sort matches alphabetically and print
matches.sort()
for match in matches:
    print(match)