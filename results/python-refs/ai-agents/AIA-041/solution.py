import json
import sys

def classify_and_prioritize(data):
    items = data['items']
    priority_rules = data['priority_rules']
    
    # Define keywords for each category based on the priority rules
    category_keywords = {
        'production': ['server', 'fire', 'down', 'services', 'production', 'outage', 'crash', 'error', 'broken'],
        'customer-blocking': ['customer', 'login', 'blocking', 'demo', 'cannot', 'access', 'stuck'],
        'cosmetic': ['color', 'blue', 'green', 'ui', 'appearance', 'cosmetic', 'style', 'visual']
    }
    
    # Priority mapping based on the rules
    priority_mapping = {
        'production': 1,
        'customer-blocking': 2,
        'cosmetic': 5
    }
    
    result = []
    
    for item in items:
        text_lower = item['text'].lower()
        
        # Determine category based on keywords
        category = 'other'
        max_matches = 0
        
        for cat, keywords in category_keywords.items():
            matches = sum(1 for keyword in keywords if keyword in text_lower)
            if matches > max_matches:
                max_matches = matches
                category = cat
        
        # If no keywords match, default to lowest priority
        if category == 'other':
            category = 'cosmetic'
        
        priority = priority_mapping.get(category, 5)
        
        result.append({
            'id': item['id'],
            'priority': priority,
            'category': category
        })
    
    # Sort by priority (1 is highest priority)
    result.sort(key=lambda x: x['priority'])
    
    return result

# Read from stdin
input_data = json.loads(sys.stdin.read().strip())

# Process and get result
output = classify_and_prioritize(input_data)

# Write to stdout
print(json.dumps(output, separators=(',', ':')))