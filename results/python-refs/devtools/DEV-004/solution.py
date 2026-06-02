import sys
from collections import defaultdict

def main():
    commits = defaultdict(list)
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
            
        # Parse the line: YYYY-MM-DD <type>: <message>
        parts = line.split(' ', 2)
        if len(parts) < 3:
            continue
            
        date = parts[0]
        type_and_colon = parts[1]
        message = parts[2]
        
        # Extract type (remove the colon)
        if type_and_colon.endswith(':'):
            commit_type = type_and_colon[:-1]
        else:
            continue
            
        commits[commit_type].append(message)
    
    # Print changelog
    print("## Unreleased")
    print()
    
    # Define type order and their display names
    type_mapping = {
        'feat': 'Features',
        'fix': 'Bug Fixes',
        'chore': 'Chore',
        'docs': 'Documentation',
        'refactor': 'Refactor'
    }
    
    type_order = ['feat', 'fix', 'chore', 'docs', 'refactor']
    
    for commit_type in type_order:
        if commit_type in commits:
            print(f"### {type_mapping[commit_type]}")
            for message in commits[commit_type]:
                print(f"- {message}")
            print()

if __name__ == "__main__":
    main()