import sys
import re

# Read all input from stdin
text = sys.stdin.read()

# Count characters
char_count = len(text)

# Count words (sequences of non-whitespace characters)
words = text.split()
word_count = len(words)

# Count sentences (ending with . ! or ?)
sentence_count = len(re.findall(r'[.!?]', text))

# Count paragraphs (separated by blank lines)
# Split by double newlines and filter out empty strings
paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
paragraph_count = len(paragraphs)

# Calculate average word length
if word_count > 0:
    # Remove punctuation from words to get actual word characters
    clean_words = [re.sub(r'[^\w]', '', word) for word in words]
    total_word_chars = sum(len(word) for word in clean_words)
    avg_word_length = total_word_chars / word_count
else:
    avg_word_length = 0.0

# Output in the required format
print(f"chars: {char_count}")
print(f"words: {word_count}")
print(f"sentences: {sentence_count}")
print(f"paragraphs: {paragraph_count}")
print(f"avg_word_length: {avg_word_length}")