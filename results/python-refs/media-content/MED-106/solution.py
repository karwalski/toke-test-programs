import sys
import re

text = sys.stdin.read().strip()
matches = re.findall(r'"([^"]*)"', text)
for match in matches:
    print(match)