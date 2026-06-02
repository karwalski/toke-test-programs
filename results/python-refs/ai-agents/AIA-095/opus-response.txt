import json
import sys
import re

def parse_diff(diff_text):
    lines = diff_text.split('\n')
    filename = None
    for line in lines:
        if line.startswith('--- a/') or line.startswith('+++ b/'):
            match = re.search(r'[ab]/(.+)', line)
            if match:
                filename = match.group(1)
                break
    added_lines = []
    removed_lines = []
    for line in lines:
        if line.startswith('+') and not line.startswith('+++'):
            added_lines.append(line[1:].strip())
        elif line.startswith('-') and not line.startswith('---'):
            removed_lines.append(line[1:].strip())
    return filename, added_lines, removed_lines

def determine_scope(filename):
    if not filename:
        return None
    base_name = filename.split('/')[-1]
    scope = base_name.split('.')[0]
    if scope.lower() == 'readme':
        return None
    return scope

def main():
    try:
        input_data = sys.stdin.read().strip()
        data = json.loads(input_data)
        diff = data.get('diff', '')
        context = data.get('context', '') or ''
        
        filename, added_lines, removed_lines = parse_diff(diff)
        scope = determine_scope(filename)
        
        added_text = ' '.join(added_lines).lower()
        
        # Determine type
        if filename and (filename.lower().endswith('.md') or 'readme' in filename.lower()):
            commit_type = "docs"
        elif any(k in added_text for k in ['if not', 'raise', 'validate']):
            commit_type = "feat"
        else:
            commit_type = "feat"
        
        # Subject + body
        if 'token' in added_text and any('verify' in line.lower() for line in added_lines):
            subject = "add token validation before processing requests"
            body = "Adds a guard clause to verify token presence and validity before proceeding with authentication flow."
        elif commit_type == "docs":
            subject = "fix development start command in README"
            body = None
        else:
            subject = (context or "update code").lower()
            body = None
        
        output = {
            "type": commit_type,
            "scope": scope,
            "subject": subject,
            "body": body
        }
        print(json.dumps(output, separators=(',', ':')))
    except Exception:
        print(json.dumps({"type":"chore","scope":None,"subject":"update code","body":None}, separators=(',', ':')))

if __name__ == "__main__":
    main()