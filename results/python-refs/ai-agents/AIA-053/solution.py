import re
import json
import sys

def get_context(text, start, end, value):
    # Get ~5 words around the link (including the link itself)
    # Find words before and after
    before_text = text[:start]
    after_text = text[end:]
    
    # Get words before
    before_words = re.findall(r'\S+', before_text)
    # Get words after  
    after_words = re.findall(r'\S+', after_text)
    
    # Try different splits to find ~5 words total context
    # Aim for value + some before + some after = ~5 words
    # Try taking up to N before and fill rest after, total 5 words
    
    best_context = None
    # Try various combinations - prefer ones starting with words before
    for n_before in range(min(len(before_words), 4), -1, -1):
        n_after = 5 - 1 - n_before  # value counts as 1 word
        if n_after < 0:
            n_after = 0
        n_after = min(n_after, len(after_words))
        
        parts = []
        if n_before > 0:
            parts.extend(before_words[-n_before:])
        parts.append(value)
        if n_after > 0:
            parts.extend(after_words[:n_after])
        
        ctx = ' '.join(parts)
        # Strip trailing punctuation
        ctx = ctx.rstrip('.!?,;:')
        if best_context is None:
            best_context = ctx
    
    return best_context

def extract_links_with_context(text):
    results = []
    
    url_pattern = r'https?://[^\s]+?(?=[\s.,;!?]*(?:\s|$))'
    # simpler: match URL stopping at whitespace, then strip trailing punctuation
    
    matches = []
    
    for match in re.finditer(r'https?://\S+', text):
        value = match.group()
        # strip trailing punctuation
        stripped = value.rstrip('.,;!?')
        start = match.start()
        end = start + len(stripped)
        matches.append((start, end, 'url', stripped))
    
    for match in re.finditer(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', text):
        # Skip if inside a URL
        s, e = match.span()
        in_url = any(ms <= s < me for ms, me, t, v in matches if t == 'url')
        if in_url:
            continue
        matches.append((s, e, 'email', match.group()))
    
    for match in re.finditer(r'\+?\d{1,3}[-.]?\d{3}[-.]?\d{4}', text):
        s, e = match.span()
        matches.append((s, e, 'phone', match.group()))
    
    matches.sort()
    
    for start, end, typ, value in matches:
        context = get_context(text, start, end, value)
        results.append({
            "type": typ,
            "value": value,
            "context": context
        })
    
    return results

text = sys.stdin.read().strip()
links = extract_links_with_context(text)
print(json.dumps(links, separators=(',', ':')))