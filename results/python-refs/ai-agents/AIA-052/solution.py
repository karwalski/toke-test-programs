import sys
import json
import re

def extract_action_items(text):
    action_items = []
    lines = text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line or not line.startswith('-'):
            continue
            
        # Remove the bullet point
        line = line[1:].strip()
        
        # Pattern to match action items with assignee
        # Look for patterns like "Name will/needs to/to do something"
        patterns = [
            r'^(\w+)\s+will\s+(.+?)(?:\s+by\s+(.+))?$',
            r'^(\w+)\s+needs\s+to\s+(.+?)(?:\s+(before\s+.+))?$',
            r'^(\w+)\s+to\s+(.+)$'
        ]
        
        for pattern in patterns:
            match = re.match(pattern, line, re.IGNORECASE)
            if match:
                assignee = match.group(1)
                task = match.group(2).strip()
                deadline = None
                
                if len(match.groups()) > 2 and match.group(3):
                    deadline = match.group(3).strip()
                
                action_items.append({
                    "assignee": assignee,
                    "task": task,
                    "deadline": deadline
                })
                break
    
    return action_items

# Read input from stdin
input_text = sys.stdin.read()

# Extract action items
action_items = extract_action_items(input_text)

# Output as JSON
print(json.dumps(action_items, separators=(',', ':')))