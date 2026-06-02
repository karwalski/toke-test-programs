import sys
import re

lines = sys.stdin.read().strip().split('\n')

pattern = lines[0]
invert = False
data_start_index = 1

# Check if second line is 'invert' flag
if len(lines) > 1 and lines[1] == 'invert':
    invert = True
    data_start_index = 2

# Compile the regex pattern
regex = re.compile(pattern)

# Process data lines
for i in range(data_start_index, len(lines)):
    line = lines[i]
    matches = regex.search(line) is not None
    
    if (matches and not invert) or (not matches and invert):
        print(line)