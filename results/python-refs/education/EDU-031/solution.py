import sys

# Read the first line for min and max word counts
first_line = input().strip()
min_words, max_words = map(int, first_line.split())

# Read the rest of the input (essay text)
essay_text = ""
try:
    while True:
        line = input()
        essay_text += line + " "
except EOFError:
    pass

# Count words in the essay
words = essay_text.split()
word_count = len(words)

# Check if it meets requirements
if min_words <= word_count <= max_words:
    print(f"PASS: {word_count} words")
else:
    print(f"FAIL: {word_count} words (min {min_words}, max {max_words})")