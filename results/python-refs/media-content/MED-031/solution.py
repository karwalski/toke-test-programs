import sys
import re

# Read input
lines = sys.stdin.read().strip().split('\n')
pattern = lines[0]
color_code = lines[1]
text = '\n'.join(lines[2:])

# Apply color wrapping to matching words
def wrap_matches(match):
    return f"\033[{color_code}m{match.group()}\033[0m"

result = re.sub(pattern, wrap_matches, text)
print(result)