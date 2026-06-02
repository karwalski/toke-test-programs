import sys
import re

def html_to_markdown(html):
    html = html.strip()
    
    # Headers
    for i in range(6, 0, -1):
        hashes = '#' * i
        html = re.sub(rf'<h{i}>(.*?)</h{i}>', rf'{hashes} \1\n\n', html, flags=re.DOTALL)
    
    # Bold
    html = re.sub(r'<(b|strong)>(.*?)</\1>', r'**\2**', html, flags=re.DOTALL)
    # Italic
    html = re.sub(r'<(i|em)>(.*?)</\1>', r'*\2*', html, flags=re.DOTALL)
    
    # Links
    html = re.sub(r'<a\s+href="([^"]*)"[^>]*>(.*?)</a>', r'[\2](\1)', html, flags=re.DOTALL)
    
    # Code and pre
    html = re.sub(r'<pre>(.*?)</pre>', r'```\n\1\n```', html, flags=re.DOTALL)
    html = re.sub(r'<code>(.*?)</code>', r'`\1`', html, flags=re.DOTALL)
    
    # Lists - handle ul
    def replace_ul(match):
        content = match.group(1)
        items = re.findall(r'<li>(.*?)</li>', content, flags=re.DOTALL)
        return '\n'.join(f'- {it}' for it in items) + '\n\n'
    
    def replace_ol(match):
        content = match.group(1)
        items = re.findall(r'<li>(.*?)</li>', content, flags=re.DOTALL)
        return '\n'.join(f'{i+1}. {it}' for i, it in enumerate(items)) + '\n\n'
    
    html = re.sub(r'<ul>(.*?)</ul>', replace_ul, html, flags=re.DOTALL)
    html = re.sub(r'<ol>(.*?)</ol>', replace_ol, html, flags=re.DOTALL)
    
    # Paragraphs
    html = re.sub(r'<p>(.*?)</p>', r'\1\n\n', html, flags=re.DOTALL)
    
    # Line breaks
    html = re.sub(r'<br\s*/?>', '\n', html)
    
    # Strip trailing whitespace/newlines
    html = html.rstrip()
    
    return html

input_html = sys.stdin.read()
print(html_to_markdown(input_html))