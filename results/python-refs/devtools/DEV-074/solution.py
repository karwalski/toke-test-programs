import sys
import re

# Read all input from stdin
text = sys.stdin.read()

# Count characters
char_count = len(text)

# Count words (split on whitespace)
words = text.split()
word_count = len(words)

# Approximate GPT-style token count
# GPT tokens are roughly 4 characters on average for English text
# But we need to account for punctuation and special characters
# A simple heuristic: count words + punctuation marks as separate tokens
punctuation_count = len(re.findall(r'[^\w\s]', text))
approx_tokens = word_count + punctuation_count

# Output in exact format
print(f"chars: {char_count}")
print(f"words: {word_count}")
print(f"approx_tokens: {approx_tokens}")