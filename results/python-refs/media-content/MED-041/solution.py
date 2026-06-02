import sys

lines = sys.stdin.read().strip().split('\n')
max_length = int(lines[0])

for i in range(1, len(lines)):
    text = lines[i]
    if len(text) <= max_length:
        print(text)
    else:
        truncated = text[:max_length-3] + '...'
        print(truncated)