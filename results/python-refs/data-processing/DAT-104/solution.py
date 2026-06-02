import sys
import json
import re

def parse_properties():
    properties = {}
    content = sys.stdin.read()
    lines = content.splitlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip empty lines and comments
        if not line or line.startswith('#') or line.startswith('!'):
            i += 1
            continue
        
        # Handle line continuation (backslash at end)
        while line.endswith('\\'):
            line = line[:-1]  # Remove the backslash
            i += 1
            if i < len(lines):
                line += lines[i].strip()
        
        # Find the separator (= or :)
        sep_idx = -1
        for j, char in enumerate(line):
            if char in '=:' and (j == 0 or line[j-1] != '\\'):
                sep_idx = j
                break
        
        if sep_idx != -1:
            key = line[:sep_idx].strip()
            value = line[sep_idx + 1:].strip()
            
            # Process unicode escapes and other escape sequences
            key = process_escapes(key)
            value = process_escapes(value)
            
            properties[key] = value
        
        i += 1
    
    return properties

def process_escapes(text):
    # Handle unicode escapes (\uXXXX)
    def replace_unicode(match):
        hex_digits = match.group(1)
        return chr(int(hex_digits, 16))
    
    text = re.sub(r'\\u([0-9a-fA-F]{4})', replace_unicode, text)
    
    # Handle other escape sequences
    text = text.replace('\\n', '\n')
    text = text.replace('\\r', '\r')
    text = text.replace('\\t', '\t')
    text = text.replace('\\f', '\f')
    text = text.replace('\\\\', '\\')
    text = text.replace('\\=', '=')
    text = text.replace('\\:', ':')
    text = text.replace('\\ ', ' ')
    
    return text

# Parse properties and output as JSON
properties = parse_properties()
print(json.dumps(properties, separators=(',', ':'), sort_keys=True))