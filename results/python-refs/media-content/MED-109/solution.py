import sys
import re

# Read all input from stdin
text = sys.stdin.read()

# Remove control characters (ASCII 0-31 except LF) and DEL (127)
# Keep LF (10) for now to handle line ending normalization
cleaned = ''.join(char for char in text if ord(char) >= 32 or char == '\n')

# Normalize line endings: CRLF to LF (already done since we removed CR)
# Remove all remaining whitespace including newlines
cleaned = re.sub(r'\s', '', cleaned)

# Write to stdout
sys.stdout.write(cleaned)