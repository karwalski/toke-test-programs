import sys

text = sys.stdin.read().strip()
words = text.split()

if len(words) == 0:
    ttr = 0.0
else:
    unique_words = len(set(words))
    total_words = len(words)
    ttr = unique_words / total_words

print(f"ttr: {ttr:.3f}")