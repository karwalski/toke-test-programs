import sys
import re

def escape_html(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def process_inline(text):
    # Handle bold text
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    return text

def markdown_to_html(markdown):
    lines = markdown.strip().split('\n')
    html_lines = []
    in_list = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Skip empty lines
        if not line.strip():
            i += 1
            continue
            
        # Handle headers
        if line.startswith('#'):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            level = len(line) - len(line.lstrip('#'))
            text = line[level:].strip()
            text = escape_html(text)
            text = process_inline(text)
            html_lines.append(f'<h{level}>{text}</h{level}>')
        
        # Handle list items
        elif line.startswith('- '):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            text = line[2:].strip()
            text = escape_html(text)
            text = process_inline(text)
            html_lines.append(f'<li>{text}</li>')
        
        # Handle paragraphs
        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            text = escape_html(line.strip())
            text = process_inline(text)
            html_lines.append(f'<p>{text}</p>')
        
        i += 1
    
    # Close any open list
    if in_list:
        html_lines.append('</ul>')
    
    return '\n'.join(html_lines)

# Read from stdin
markdown_content = sys.stdin.read()

# Convert to HTML
body_html = markdown_to_html(markdown_content)

# Create complete HTML5 document
html_output = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body>
{body_html}
</body>
</html>"""

print(html_output)