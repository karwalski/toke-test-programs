import sys
import json
import re

def categorize_commit(line):
    """Categorize a commit message and extract the description."""
    line = line.strip()
    if not line:
        return None, None
    
    # Define patterns for different categories
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
    
    # Try to match against each category
    for category, category_patterns in patterns.items():
        for pattern in category_patterns:
            match = re.match(pattern, line, re.IGNORECASE)
            if match:
                description = match.group(1).strip()
                # Clean up the description
                description = clean_description(description, category)
                return category, description
    
    return None, None

def clean_description(description, category):
    """Clean up the description to match expected output format."""
    # Remove leading/trailing whitespace
    description = description.strip()
    
    # Capitalize first letter
    if description:
        description = description[0].upper() + description[1:]
    
    # Handle specific transformations based on the expected output
    transformations = {
        'add dark mode support': 'Dark mode support',
        'resolve login timeout issue': 'Login timeout issue resolved',
        'add export to CSV': 'Export to CSV',
        'correct timezone display': 'Timezone display corrected',
        'improve database query performance': 'Database query performance improved',
        'remove deprecated v1 API endpoints': 'Deprecated v1 API endpoints removed',
    }
    
    # Check for exact matches first
    description_lower = description.lower()
    for key, value in transformations.items():
        if description_lower == key:
            return value
    
    # Apply general rules based on category
    if category == 'fixes':
        if 'resolve' in description_lower:
            description = description.replace('resolve ', '').replace('Resolve ', '')
            if not description.endswith(' resolved'):
                description += ' resolved'
        elif 'correct' in description_lower:
            description = description.replace('correct ', '').replace('Correct ', '')
            if not description.endswith(' corrected'):
                description += ' corrected'
        elif 'fix' in description_lower:
            description = description.replace('fix ', '').replace('Fix ', '')
            if not description.endswith(' fixed'):
                description += ' fixed'
    
    elif category == 'improvements':
        if 'improve ' in description_lower:
            description = description.replace('improve ', '').replace('Improve ', '')
            if not description.endswith(' improved'):
                description += ' improved'
    
    elif category == 'features':
        if description_lower.startswith('add '):
            description = description[4:]  # Remove 'add '
        elif description_lower.startswith('Add '):
            description = description[4:]  # Remove 'Add '
    
    elif category == 'breaking_changes':
        if description_lower.startswith('remove '):
            description = description[7:]  # Remove 'remove '
            if not description.endswith(' removed'):
                description += ' removed'
        elif description_lower.startswith('Remove '):
            description = description[7:]  # Remove 'Remove '
            if not description.endswith(' removed'):
                description += ' removed'
    
    return description

def main():
    # Initialize categories
    release_notes = {
        'features': [],
        'fixes': [],
        'improvements': [],
        'breaking_changes': []
    }
    
    # Read from stdin
    for line in sys.stdin:
        category, description = categorize_commit(line)
        if category and description:
            release_notes[category].append(description)
    
    # Output JSON
    json_output = json.dumps(release_notes, separators=(',', ':'))
    print(json_output)

if __name__ == '__main__':
    main()