import json
import sys
import re

def extract_comments(code, language):
    lines = code.split('\n')
    comments = []
    
    # Define comment patterns for different languages
    comment_patterns = {
        'python': r'^\s*#\s*(.*)',
        'javascript': r'^\s*//\s*(.*)',
        'java': r'^\s*//\s*(.*)',
        'c': r'^\s*//\s*(.*)',
        'cpp': r'^\s*//\s*(.*)',
        'c++': r'^\s*//\s*(.*)',
    }
    
    # Get the appropriate pattern for the language
    pattern = comment_patterns.get(language.lower(), r'^\s*#\s*(.*)')
    
    for i, line in enumerate(lines, 1):
        # Check for inline comments (comments at the end of a line with code)
        if language.lower() == 'python':
            inline_match = re.search(r'[^#\s].*?#\s*(.*)', line)
            if inline_match:
                comment_text = inline_match.group(1).strip()
                if comment_text:
                    comment_type = categorize_comment(comment_text)
                    comments.append({
                        "type": comment_type,
                        "text": comment_text,
                        "line_number": i
                    })
                continue
        
        # Check for full-line comments
        match = re.match(pattern, line)
        if match:
            comment_text = match.group(1).strip()
            if comment_text:
                comment_type = categorize_comment(comment_text)
                comments.append({
                    "type": comment_type,
                    "text": comment_text,
                    "line_number": i
                })
    
    return comments

def categorize_comment(text):
    text_upper = text.upper()
    
    if text_upper.startswith('TODO:'):
        return 'todo'
    elif text_upper.startswith('FIXME:'):
        return 'fixme'
    elif text_upper.startswith('TODO '):
        return 'todo'
    elif text_upper.startswith('FIXME '):
        return 'fixme'
    
    # Check if it's a TODO or FIXME without colon
    if re.match(r'^TODO\b', text_upper):
        return 'todo'
    elif re.match(r'^FIXME\b', text_upper):
        return 'fixme'
    
    # Default to documentation for full-line comments, inline for others
    return 'documentation'

def main():
    input_data = json.loads(sys.stdin.read())
    code = input_data['code']
    language = input_data['language']
    
    comments = extract_comments(code, language)
    
    # Process comments to clean up text and determine correct type
    processed_comments = []
    for comment in comments:
        text = comment['text']
        
        # Check if this is an inline comment (heuristic based on line content)
        lines = code.split('\n')
        line_content = lines[comment['line_number'] - 1] if comment['line_number'] <= len(lines) else ""
        
        # Determine if inline by checking if there's code before the comment
        is_inline = False
        if language.lower() == 'python':
            if re.search(r'[^#\s].*?#', line_content):
                is_inline = True
        
        # Clean up TODO/FIXME text
        if text.upper().startswith('TODO:'):
            comment_type = 'todo'
            clean_text = text[5:].strip()
        elif text.upper().startswith('FIXME:'):
            comment_type = 'fixme'
            clean_text = text[6:].strip()
        elif re.match(r'^TODO\b', text.upper()):
            comment_type = 'todo'
            clean_text = re.sub(r'^TODO\s*:?\s*', '', text, flags=re.IGNORECASE).strip()
        elif re.match(r'^FIXME\b', text.upper()):
            comment_type = 'fixme'
            clean_text = re.sub(r'^FIXME\s*:?\s*', '', text, flags=re.IGNORECASE).strip()
        else:
            clean_text = text
            if is_inline:
                comment_type = 'inline'
            else:
                comment_type = 'documentation'
        
        processed_comments.append({
            "type": comment_type,
            "text": clean_text,
            "line_number": comment['line_number']
        })
    
    print(json.dumps(processed_comments, separators=(',', ':')))

if __name__ == "__main__":
    main()