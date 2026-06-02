import sys

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.strip())

search_text = lines[0]
dictionary_words = lines[1:]

# Find all occurrences
results = []

for word in dictionary_words:
    for i in range(len(search_text) - len(word) + 1):
        if search_text[i:i+len(word)] == word:
            results.append((i, word))

# Sort by position then alphabetically
results.sort(key=lambda x: (x[0], x[1]))

# Output
for pos, word in results:
    print(f"{word} at {pos}")