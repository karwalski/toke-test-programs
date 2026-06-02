import sys
import re

# Read input from stdin
input_text = sys.stdin.read().strip()

# Find all markdown links using regex
# Pattern matches [text](url) format
pattern = r'\[([^\]]+)\]\(([^)]+)\)'
matches = re.findall(pattern, input_text)

# Output numbered list
for i, (text, url) in enumerate(matches, 1):
    print(f"{i}. [{text}]({url})")