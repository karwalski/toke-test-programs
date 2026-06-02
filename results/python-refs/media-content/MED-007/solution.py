import sys

text = sys.stdin.read()

# Count words
words = len(text.split())

# Count lines
lines = len(text.splitlines())

# Count characters
chars = len(text)

print(f"words: {words}")
print(f"lines: {lines}")
print(f"chars: {chars}")