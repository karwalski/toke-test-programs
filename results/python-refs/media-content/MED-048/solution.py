import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

for line in reversed(lines):
    print(line)