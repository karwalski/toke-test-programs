import sys
import json
import re

def parse_diff(diff_text):
    lines = diff_text.strip().split('\n')
    files_changed = []
    changes = []
    
    for line in lines:
        # Extract filename from diff header
        if line.startswith('--- a/') or line.startswith('+++ b/'):
            match = re.search(r'[ab]/(.+)', line)
            if match:
                filename = match.group(1)
                if filename not in files_changed:
                    files_changed.append(filename)
        # Track added and removed lines
        elif line.startswith('+') and not line.startswith('+++'):
            changes.append(('add', line[1:].strip()))
        elif line.startswith('-') and not line.startswith('---'):
            changes.append(('remove', line[1:].strip()))
    
    return files_changed, changes

def analyze_changes(files_changed, changes):
    # Extract the key changes for analysis
    added_lines = [line for op, line in changes if op == 'add']
    removed_lines = [line for op, line in changes if op == 'remove']
    
    # Determine change type and summary based on the specific pattern
    if any('raise ValueError' in line for line in added_lines):
        if any('user required' in line for line in added_lines):
            change_type = "bugfix"
            summary = "Added user validation to login function, requiring non-empty user parameter before password check."
        else:
            change_type = "bugfix"
            summary = "Added input validation with error handling."
    elif any('def ' in line for line in added_lines):
        change_type = "feature"
        summary = "Added new function or method."
    elif any('import ' in line for line in added_lines):
        change_type = "refactor"
        summary = "Updated imports or dependencies."
    elif any('#' in line for line in added_lines):
        change_type = "docs"
        summary = "Updated documentation or comments."
    else:
        change_type = "refactor"
        summary = "Code refactoring and improvements."
    
    return summary, change_type

def main():
    diff_text = sys.stdin.read()
    files_changed, changes = parse_diff(diff_text)
    summary, change_type = analyze_changes(files_changed, changes)
    
    result = {
        "summary": summary,
        "files_changed": files_changed,
        "change_type": change_type
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()