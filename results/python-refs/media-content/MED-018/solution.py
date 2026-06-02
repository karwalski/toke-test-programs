import sys
import re

# Read all input
content = sys.stdin.read()

# Split into lines
lines = content.strip().split('\n')

# Find footnote definitions
footnote_defs = {}
body_lines = []

for line in lines:
    # Check if line is a footnote definition
    match = re.match(r'^\[\^(\d+)\]:\s*(.*)$', line)
    if match:
        footnote_num = match.group(1)
        footnote_text = match.group(2)
        footnote_defs[footnote_num] = footnote_text
    else:
        body_lines.append(line)

# Process body text to replace footnote markers
body_text = '\n'.join(body_lines)

# Replace [^N] with [N]
def replace_marker(match):
    num = match.group(1)
    return f'[{num}]'

body_text = re.sub(r'\[\^(\d+)\]', replace_marker, body_text)

# Output body text
print(body_text)

# Output references section if there are footnotes
if footnote_defs:
    print()
    print("References:")
    for num in sorted(footnote_defs.keys(), key=int):
        print(f"{num}. {footnote_defs[num]}")