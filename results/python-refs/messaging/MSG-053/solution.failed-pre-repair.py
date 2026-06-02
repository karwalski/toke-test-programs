import sys
import re

def convert_markdown_to_plain(text):
    lines = text.split('\n')
    result = []
    
    for line in lines:
        # Handle headers - convert to uppercase and remove # symbols
        if line.startswith('#'):
            # Remove all # symbols and leading/trailing whitespace
            header_text = re.sub(r'^#+\s*', '', line).strip()
            result.append(header_text.upper())
        
        # Handle code blocks - replace