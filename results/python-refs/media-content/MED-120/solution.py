import json
import sys
import re

# Read the first line as JSON
abbreviations = json.loads(input().strip())

# Read the remaining text
text_lines = []
for line in sys.stdin:
    text_lines.append(line.rstrip('\n'))

text = '\n'.join(text_lines)

# Replace abbreviations with their expansions
for abbrev, expansion in abbreviations.items():
    # Use word boundaries to match whole words only
    pattern = r'\b' + re.escape(abbrev) + r'\b'
    text = re.sub(pattern, expansion, text, flags=re.IGNORECASE)

print(text)