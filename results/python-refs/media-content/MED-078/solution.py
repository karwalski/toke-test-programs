import sys
import re

text = sys.stdin.read().strip()

# Remove all markdown emphasis markers in order of precedence
# First remove triple markers, then double, then single
text = re.sub(r'\*\*\*(.*?)\*\*\*', r'\1', text)
text = re.sub(r'___(.*?)___', r'\1', text)
text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
text = re.sub(r'__(.*?)__', r'\1', text)
text = re.sub(r'\*(.*?)\*', r'\1', text)
text = re.sub(r'_(.*?)_', r'\1', text)

print(text)