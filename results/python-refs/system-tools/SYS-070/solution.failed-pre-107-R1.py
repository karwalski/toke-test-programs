import re
import sys

# Read the regex pattern from the first line
pattern = input().strip()

# Read all remaining text from stdin
text = sys.stdin.read()

# Find all non-overlapping matches
matches = re.findall(pattern, text)

# Output each match on its own line
for match in matches:
    print(match)