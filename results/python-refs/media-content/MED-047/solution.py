import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

lines.sort()

for line in lines:
    print(line)