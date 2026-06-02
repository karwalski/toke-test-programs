import sys
import re

# Read all input from stdin
text = sys.stdin.read()

# Find all bold text patterns (**text**)
pattern = r'\*\*([^*]+)\*\*'
matches = re.findall(pattern, text)

# Output each match on a separate line
for match in matches:
    print(match)