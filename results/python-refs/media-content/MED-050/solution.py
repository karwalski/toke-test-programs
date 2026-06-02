import sys
import json

def parse_yaml_frontmatter(content):
    lines = content.split('\n')
    
    if not lines or lines[0] != '---':
        return {}, content
    
    # Find the closing ---
    end_idx = -1
    for i in range(1, len(lines)):
        if lines[i] == '---':
            end_idx = i
            break
    
    if end_idx == -1:
        return {}, content
    
    # Parse the YAML front matter
    frontmatter = {}
    for i in range(1, end_idx):
        line = lines[i].strip()
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            frontmatter[key] = value
    
    # Get the body (everything after the closing ---)
    body_lines = lines[end_idx + 1:]
    body = '\n'.join(body_lines)
    
    return frontmatter, body

# Read from stdin
content = sys.stdin.read()

# Parse the content
frontmatter, body = parse_yaml_frontmatter(content)

# Output JSON front matter
print(json.dumps(frontmatter, separators=(',', ':')))

# Output blank line
print()

# Output body
print(body, end='')