import sys
import re

def html_to_markdown(html):
    # Remove extra whitespace and newlines
    html = html.strip()
    
    # Convert headers
    html = re.sub(r'<h1>(.*?)</h1>', r'# \1', html)
    html = re.sub(r'<h2>(.*?)</h2>', r'## \1', html)
    html = re.sub(r'<h3>(.*?)</h3>', r'### \1', html)
    html = re.sub(r'<h4>(.*?)</h4>', r'#### \1', html)
    html = re.sub(r'<h5>(.*?)</h5>', r'##### \1', html)
    html = re.sub(r'<h6>(.*?)</h6>', r'###### \1', html)
    
    # Convert bold tags
    html = re.sub(r'<b>(.*?)</b>', r'**\1**', html)
    html = re.sub(r'<strong>(.*?)</strong>', r'**\1**', html)
    
    # Convert italic tags
    html = re.sub(r'<i>(.*?)</i>', r'*\1*', html)
    html = re.sub(r'<em>(.*?)</em>', r'*\1*', html)
    
    # Convert paragraphs
    html = re.sub(r'<p>(.*?)</p>', r'\1', html)
    
    # Convert line breaks
    html = re.sub(r'<br\s*/?>', '\n', html)
    
    # Add proper spacing between block elements
    # Split by headers and add blank lines
    lines = []
    parts = html.split('>')
    current_line = ""
    
    for i, part in enumerate(parts):
        if i == len(parts) - 1:
            current_line += part
            break
            
        if part.endswith('#'):
            # This is a header
            if current_line.strip():
                lines.append(current_line.strip())
                current_line = ""
            current_line += part + '>'
        else:
            current_line += part + '>'
    
    if current_line.strip():
        lines.append(current_line.strip())
    
    # Process the HTML string to add proper line breaks
    result = html
    
    # Add blank line after headers
    result = re.sub(r'(# .+)', r'\1\n', result)
    result = re.sub(r'(## .+)', r'\1\n', result)
    result = re.sub(r'(### .+)', r'\1\n', result)
    result = re.sub(r'(#### .+)', r'\1\n', result)
    result = re.sub(r'(##### .+)', r'\1\n', result)
    result = re.sub(r'(###### .+)', r'\1\n', result)
    
    return result

# Read input from stdin
input_html = sys.stdin.read().strip()

# Convert to markdown
markdown = html_to_markdown(input_html)

# Print the result
print(markdown)