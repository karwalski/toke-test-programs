import re
import sys
from urllib.parse import urlparse

def detect_content_type(message):
    message = message.strip()
    
    # Check if it's a URL
    url_pattern = r'^https?://[^\s]+$'
    if re.match(url_pattern, message):
        try:
            parsed = urlparse(message)
            domain = parsed.netloc
            return f"url: {message} [domain={domain}]"
        except:
            return f"url: {message}"
    
    # Check if it's emoji-only (simple emoticons)
    emoji_pattern = r'^[:;][)(:D]+$|^[)(:D;:]+$'
    if re.match(emoji_pattern, message):
        # Count individual emoji characters
        emoji_chars = re.findall(r'[:;][)(:D]|[)(:D]', message)
        # For patterns like :):):), count the number of complete emoticons
        complete_emoticons = re.findall(r'[:;][)(:D]', message)
        if complete_emoticons:
            count = len(complete_emoticons)
        else:
            # Count individual characters that could be emoticons
            count = len([c for c in message if c in ')(:D'])
        
        # Special handling for :):):) pattern
        if ':):):)' in message:
            count = message.count(':)')
        
        return f"emoji: {message} [count={count}]"
    
    # Check if it's code
    code_indicators = [
        r'function\s+\w+\s*\([^)]*\)\s*{',  # JavaScript function
        r'def\s+\w+\s*\([^)]*\)\s*:',       # Python function
        r'class\s+\w+\s*{',                 # Class definition
        r'if\s*\([^)]+\)\s*{',              # If statement
        r'for\s*\([^)]+\)\s*{',             # For loop
        r'while\s*\([^)]+\)\s*{',           # While loop
        r'return\s+[^;]+[;}]',              # Return statement
    ]
    
    for pattern in code_indicators:
        if re.search(pattern, message):
            # Detect language based on patterns
            if re.search(r'function\s+\w+\s*\([^)]*\)\s*{', message):
                return f"code: {message} [lang=javascript]"
            elif re.search(r'def\s+\w+\s*\([^)]*\)\s*:', message):
                return f"code: {message} [lang=python]"
            else:
                return f"code: {message} [lang=javascript]"  # Default to javascript
    
    # Default to text
    return f"text: {message}"

# Read from stdin and process each line
for line in sys.stdin:
    if line.strip():  # Skip empty lines
        result = detect_content_type(line)
        print(result)