import sys
import re

def minify_html(html):
    # Remove whitespace between tags
    html = re.sub(r'>\s+<', '><', html)
    
    # Collapse multiple whitespace within text content to single spaces
    # This handles spaces, tabs, newlines within tag content
    html = re.sub(r'>(\s*)(.*?)(\s*)<', lambda m: '>' + re.sub(r'\s+', ' ', m.group(2).strip()) + '<', html)
    
    return html

# Read from stdin
html_input = sys.stdin.read()

# Minify and output
minified = minify_html(html_input)
print(minified, end='')