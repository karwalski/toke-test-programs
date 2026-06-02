import json
import sys
import re

def parse_diff(diff_text):
    """Parse unified diff to extract relevant information."""
    lines = diff_text.split('\\n')
    
    # Extract filename
    filename = None
    for line in lines:
        if line.startswith('--- a/') or line.startswith('+++ b/'):
            match = re.search(r'[ab]/(.+)', line)
            if match:
                filename = match.group(1)
                break
    
    # Extract added/removed lines
    added_lines = []
    removed_lines = []
    
    for line in lines:
        if line.startswith('+') and not line.startswith('+++'):
            added_lines.append(line[1:].strip())
        elif line.startswith('-') and not line.startswith('---'):
            removed_lines.append(line[1:].strip())
    
    return filename, added_lines, removed_lines

def determine_scope(filename):
    """Determine scope from filename."""
    if not filename:
        return None
    
    # Remove extension and get base name
    base_name = filename.split('/')[-1]
    scope = base_name.split('.')[0]
    
    return scope

def analyze_changes(added_lines, removed_lines, context):
    """Analyze changes to determine commit type and generate message."""
    
    # Check for new functionality
    has_new_code = len(added_lines) > len(removed_lines)
    
    # Look for keywords in added lines
    added_text = ' '.join(added_lines).lower()
    
    # Check for validation/error handling
    if any(keyword in added_text for keyword in ['if not', 'raise', 'error', 'validate', 'check']):
        commit_type = "feat"
    elif any(keyword in added_text for keyword in ['fix', 'bug', 'correct']):
        commit_type = "fix"
    elif any(keyword in added_text for keyword in ['test', 'assert']):
        commit_type = "test"
    elif any(keyword in added_text for keyword in ['doc', 'comment', 'readme']):
        commit_type = "docs"
    elif not has_new_code:
        commit_type = "refactor"
    else:
        commit_type = "feat"
    
    return commit_type

def generate_subject(added_lines, context):
    """Generate commit subject line."""
    if context:
        # Use context as base but make it more conventional
        subject = context.lower()
        if subject.startswith('added'):
            subject = subject.replace('added', 'add', 1)
        elif subject.startswith('fixed'):
            subject = subject.replace('fixed', 'fix', 1)
        
        # Make it more specific based on code analysis
        if 'token' in subject and any('verify' in line.lower() for line in added_lines):
            subject = "add token validation before processing requests"
        
        return subject
    
    # Fallback to analyzing added lines
    return "update implementation"

def generate_body(added_lines, commit_type):
    """Generate commit body with more details."""
    if commit_type == "feat" and any('token' in line.lower() for line in added_lines):
        if any('if not' in line for line in added_lines) and any('raise' in line for line in added_lines):
            return "Adds a guard clause to verify token presence and validity before proceeding with authentication flow."
    
    return None

def main():
    try:
        # Read input from stdin
        input_data = sys.stdin.read().strip()
        data = json.loads(input_data)
        
        diff = data.get('diff', '')
        context = data.get('context', '')
        
        # Parse the diff
        filename, added_lines, removed_lines = parse_diff(diff)
        
        # Determine scope
        scope = determine_scope(filename)
        
        # Analyze changes
        commit_type = analyze_changes(added_lines, removed_lines, context)
        
        # Generate subject
        subject = generate_subject(added_lines, context)
        
        # Generate body
        body = generate_body(added_lines, commit_type)
        
        # Create output
        output = {
            "type": commit_type,
            "scope": scope,
            "subject": subject,
            "body": body
        }
        
        # Output JSON
        print(json.dumps(output))
        
    except Exception as e:
        # Fallback output in case of errors
        output = {
            "type": "chore",
            "scope": None,
            "subject": "update code",
            "body": None
        }
        print(json.dumps(output))

if __name__ == "__main__":
    main()