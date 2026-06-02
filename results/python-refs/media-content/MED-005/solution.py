import sys

text = sys.stdin.read()

# Replace special characters with HTML entities
text = text.replace('&', '&amp;')  # Must be first to avoid double-encoding
text = text.replace('<', '&lt;')
text = text.replace('>', '&gt;')
text = text.replace('"', '&quot;')
text = text.replace("'", '&#39;')

sys.stdout.write(text)