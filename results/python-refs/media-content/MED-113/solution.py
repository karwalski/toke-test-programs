import sys
import re

text = sys.stdin.read().strip()
result = re.sub(r'\^([^^]+)\^', r'<sup>\1</sup>', text)
print(result)