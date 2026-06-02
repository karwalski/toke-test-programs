import sys
import re

# Read input
lines = sys.stdin.read().strip().split('\n')
mode = lines[0]
text = '\n'.join(lines[1:])

if mode == 'to-underscore':
    # Convert **bold** to __bold__
    text = re.sub(r'\*\*([^*]+)\*\*', r'__\1__', text)
    # Convert *italic* to _italic_
    text = re.sub(r'\*([^*]+)\*', r'_\1_', text)
elif mode == 'to-asterisk':
    # Convert __bold__ to **bold**
    text = re.sub(r'__([^_]+)__', r'**\1**', text)
    # Convert _italic_ to *italic*
    text = re.sub(r'_([^_]+)_', r'*\1*', text)

print(text)