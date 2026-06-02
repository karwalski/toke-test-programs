import sys
import re

html = sys.stdin.read()
pattern = r'<a\s+[^>]*href\s*=\s*["\']([^"\']*)["\'][^>]*>'
matches = re.findall(pattern, html, re.IGNORECASE)

for url in matches:
    print(url)