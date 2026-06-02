import sys
import json
import re

def categorize_commit(line):
    line = line.strip()
    if not line:
        return None, None
    
    patterns = {
        'breaking_changes': [
            r'^BREAKING:\s*(.+)',
            r'^BREAKING CHANGE:\s*(.+)',
            r'^breaking:\s*(.+)',
        ],
        'features': [
            r'^feat:\s*(.+)',
            r'^feature:\s*(.+)',
            r'^add:\s*(.+)',
        ],
        'fixes': [
            r'^fix:\s*(.+)',
            r'^bugfix:\s*(.+)',
            r'^bug:\s*(.+)',
        ],
        'improvements': [
            r'^refactor:\s*(.+)',
            r'^improve:\s*(.+)',
            r'^enhancement:\s*(.+)',
            r'^perf:\s*(.+)',
            r'^performance:\s*(.+)',
        ]
    }
    
    for category, category_patterns in patterns.items():
        for pattern in category_patterns:
            match = re.match(pattern, line, re.IGNORECASE)
            if match:
                description = match.group(1).strip()
                description = clean_description(description, category)
                return category, description
    
    return None, None

def capitalize_first(s):
    if not s:
        return s
    return s[0].upper() + s[1:]

def clean_description(description, category):
    description = description.strip()
    desc_lower = description.lower()
    
    if category == 'fixes':
        if desc_lower.startswith('resolve '):
            description = description[8:].strip() + ' resolved'
        elif desc_lower.startswith('correct '):
            description = description[8:].strip() + ' corrected'
        elif desc_lower.startswith('fix '):
            description = description[4:].strip() + ' fixed'
    
    elif category == 'improvements':
        if desc_lower.startswith('improve '):
            description = description[8:].strip() + ' improved'
    
    elif category == 'features':
        if desc_lower.startswith('add '):
            description = description[4:].strip()
    
    elif category == 'breaking_changes':
        if desc_lower.startswith('remove '):
            description = description[7:].strip() + ' removed'
    
    return capitalize_first(description)

def main():
    release_notes = {
        'features': [],
        'fixes': [],
        'improvements': [],
        'breaking_changes': []
    }
    
    for line in sys.stdin:
        category, description = categorize_commit(line)
        if category and description:
            release_notes[category].append(description)
    
    print(json.dumps(release_notes, separators=(',', ':')))

if __name__ == '__main__':
    main()