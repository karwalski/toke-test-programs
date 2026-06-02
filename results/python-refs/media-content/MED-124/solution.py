import sys
import re

def convert_markdown_links():
    content = sys.stdin.read()
    
    # Find all reference definitions
    references = {}
    ref_pattern = r'^\[([^\]]+)\]:\s*(.+)$'
    
    lines = content.split('\n')
    output_lines = []
    
    for line in lines:
        ref_match = re.match(ref_pattern, line)
        if ref_match:
            ref_id = ref_match.group(1)
            url = ref_match.group(2).strip()
            references[ref_id] = url
        else:
            output_lines.append(line)
    
    # Convert reference-style links to inline links
    result = '\n'.join(output_lines)
    
    # Pattern to match reference-style links [text][ref]
    link_pattern = r'\[([^\]]+)\]\[([^\]]+)\]'
    
    def replace_link(match):
        text = match.group(1)
        ref_id = match.group(2)
        if ref_id in references:
            return f'[{text}]({references[ref_id]})'
        return match.group(0)  # Return original if reference not found
    
    result = re.sub(link_pattern, replace_link, result)
    
    # Remove empty lines at the end
    result = result.rstrip('\n')
    
    print(result)

if __name__ == "__main__":
    convert_markdown_links()