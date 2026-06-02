import sys
import re

def convert_admonitions(text):
    lines = text.strip().split('\n')
    result = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if line starts with NOTE:, WARNING:, or TIP:
        match = re.match(r'^(NOTE|WARNING|TIP):\s*(.*)', line)
        if match:
            admonition_type = match.group(1).lower()
            content = match.group(2)
            
            # Start the admonition block
            result.append(f'