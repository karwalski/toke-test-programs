import re
import json
import sys

def extract_links_with_context(text):
    results = []
    
    # URL pattern - matches http/https URLs
    url_pattern = r'https?://[^\s]+'
    
    # Email pattern - matches standard email format
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    # Phone pattern - matches various phone formats including +1-555-0123
    phone_pattern = r'\+?\d{1,3}[-.]?\d{3}[-.]?\d{4}'
    
    # Find URLs
    for match in re.finditer(url_pattern, text):
        start, end = match.span()
        value = match.group()
        
        # Get context - find sentence or reasonable surrounding text
        context_start = max(0, start - 50)
        context_end = min(len(text), end + 50)
        
        # Try to find word boundaries for cleaner context
        while context_start > 0 and text[context_start] not in ' \t\n.!?':
            context_start -= 1
        while context_end < len(text) and text[context_end] not in ' \t\n.!?':
            context_end += 1
            
        context = text[context_start:context_end].strip()
        
        results.append({
            "type": "url",
            "value": value,
            "context": context
        })
    
    # Find emails
    for match in re.finditer(email_pattern, text):
        start, end = match.span()
        value = match.group()
        
        # Get context
        context_start = max(0, start - 50)
        context_end = min(len(text), end + 50)
        
        while context_start > 0 and text[context_start] not in ' \t\n.!?':
            context_start -= 1
        while context_end < len(text) and text[context_end] not in ' \t\n.!?':
            context_end += 1
            
        context = text[context_start:context_end].strip()
        
        results.append({
            "type": "email",
            "value": value,
            "context": context
        })
    
    # Find phone numbers
    for match in re.finditer(phone_pattern, text):
        start, end = match.span()
        value = match.group()
        
        # Get context
        context_start = max(0, start - 50)
        context_end = min(len(text), end + 50)
        
        while context_start > 0 and text[context_start] not in ' \t\n.!?':
            context_start -= 1
        while context_end < len(text) and text[context_end] not in ' \t\n.!?':
            context_end += 1
            
        context = text[context_start:context_end].strip()
        
        results.append({
            "type": "phone",
            "value": value,
            "context": context
        })
    
    return results

# Read input from stdin
text = sys.stdin.read().strip()

# Extract links with context
links = extract_links_with_context(text)

# Output as JSON
print(json.dumps(links, separators=(',', ':')))