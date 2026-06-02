import sys

# Read all lines from stdin
lines = []
for line in sys.stdin:
    line = line.rstrip('\n')
    if line:  # Only add non-empty lines
        lines.append(line)

# Sort by first word (author last name)
lines.sort(key=lambda x: x.split(',')[0])

# Output sorted lines
for line in lines:
    print(line)