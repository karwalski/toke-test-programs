import re
import sys

html = sys.stdin.read().strip()
text = re.sub(r'<[^>]*>', '', html)
print(text)