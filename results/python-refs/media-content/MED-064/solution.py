import sys
import re

counter = 1
for line in sys.stdin:
    line = line.rstrip('\n')
    if re.match(r'^\d+\.\s', line):
        # Extract everything after the number and dot
        content = re.sub(r'^\d+\.', f'{counter}.', line)
        print(content)
        counter += 1
    else:
        print(line)