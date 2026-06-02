import sys
import re

# Read input
lines = sys.stdin.read().strip().split('\n')
tag_name = lines[0]
html = '\n'.join(lines[1:])

# Find all matching tags with attributes
pattern = f'<{tag_name}\\s+([^>]+)>'
matches = re.findall(pattern, html)

for match in matches:
    # Parse attributes from the matched string
    attr_pattern = r'(\w+)=(?:"([^"]*)"|\'([^\']*)\'|([^\s>]+))'
    attributes = re.findall(attr_pattern, match)
    
    for attr in attributes:
        attr_name = attr[0]
        attr_value = attr[1] or attr[2] or attr[3]
        print(f"{attr_name}={attr_value}")