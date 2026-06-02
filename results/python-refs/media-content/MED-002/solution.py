import sys
import re

for line in sys.stdin:
    line = line.rstrip('\n\r')
    match = re.match(r'^(#{1,6})\s+(.+)$', line)
    if match:
        level = len(match.group(1))
        text = match.group(2)
        print(f'H{level}: {text}')