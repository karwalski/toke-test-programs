import sys
import re

def extract_images(markdown_text):
    # Regular expression to match markdown image syntax
    # ![alt](src "title") or ![alt](src)
    pattern = r'!\[([^\]]*)\]\(([^\s\)]+)(?:\s+"([^"]*)")?\)'
    
    matches = re.findall(pattern, markdown_text)
    
    for match in matches:
        alt = match[0]
        src = match[1]
        title = match[2] if len(match) > 2 else ""
        
        print(f"{alt} | {src} | {title}")

# Read all input from stdin
markdown_text = sys.stdin.read()
extract_images(markdown_text)