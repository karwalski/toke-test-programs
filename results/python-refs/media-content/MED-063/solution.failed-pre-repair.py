import sys
import re

# Read all input
lines = sys.stdin.read().splitlines()

# First line is the target marker
target_marker = lines[0]

# Process remaining lines
for i in range(1, len(lines)):
    line = lines[i]
    # Replace list markers (*, +, -) followed by space at start of line
    modified_line = re.sub(r'^[*+-] ', target_marker, line)
    print(modified_line)