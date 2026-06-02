import sys
import re

text = sys.stdin.read().strip()
result = re.sub(r'~~(.*?)~~', r'<del>\1</del>', text)
print(result)