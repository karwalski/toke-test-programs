import sys

# Read target word
target_word = input().strip().upper()

# Read dictionary words
dictionary = []
for line in sys.stdin:
    word = line.strip().upper()
    if word:
        dictionary.append(word)

# Find anagrams by comparing sorted characters
target_sorted = sorted(target_word)
anagrams = []

for word in dictionary:
    if sorted(word) == target_sorted:
        anagrams.append(word)

# Sort anagrams alphabetically and output
anagrams.sort()
for anagram in anagrams:
    print(anagram)