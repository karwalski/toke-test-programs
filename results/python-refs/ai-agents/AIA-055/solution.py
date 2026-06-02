import json
import sys
import re

def categorize(text, is_inline):
    u = text.upper()
    m = re.match(r'^TODO\s*:?\s*(.*)', text, re.IGNORECASE)
    if m:
        return 'todo', m.group(1).strip()
    m = re.match(r'^FIXME\s*:?\s*(.*)', text, re.IGNORECASE)
    if m:
        return 'fixme', m.group(1).strip()
    if is_inline:
        return 'inline', text
    return 'documentation', text

def extract(code, language):
    # The input may have literal backslash-n sequences; treat actual newlines as line breaks
    lines = code.split('\n')
    comments = []
    lang = language.lower()
    
    if lang == 'python':
        marker = '#'
    else:
        marker = '//'
    
    for i, line in enumerate(lines, 1):
        idx = line.find(marker)
        if idx == -1:
            continue
        before = line[:idx]
        text = line[idx+len(marker):].strip()
        if not text:
            continue
        is_inline = bool(before.strip())
        ctype, clean = categorize(text, is_inline)
        comments.append({"type": ctype, "text": clean, "line_number": i})
    
    return comments

def main():
    data = json.loads(sys.stdin.read())
    code = data['code']
    language = data['language']
    # Handle case where code contains literal \n escapes
    if '\n' not in code and '\\n' in code:
        code = code.encode().decode('unicode_escape')
    comments = extract(code, language)
    print(json.dumps(comments, separators=(',', ':')))

if __name__ == "__main__":
    main()