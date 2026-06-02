import sys

text = sys.stdin.read().strip()
words = text.split()
unique_words = len(set(words))
print(f"unique_words: {unique_words}")