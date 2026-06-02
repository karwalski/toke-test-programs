import sys
import re

html = sys.stdin.read()

# Find all img tags with src and alt attributes
img_pattern = r'<img[^>]*src=["\']([^"\']*)["\'][^>]*alt=["\']([^"\']*)["\'][^>]*>'
matches = re.findall(img_pattern, html)

for src, alt in matches:
    print(f"{src} | {alt}")