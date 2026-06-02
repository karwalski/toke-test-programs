import json
import sys
import re

def extract_data_from_description(description, schema):
    result = {}
    
    # Get properties from schema
    properties = schema.get('properties', {})
    
    for field_name, field_schema in properties.items():
        field_type = field_schema.get('type')
        
        if field_name == 'size':
            # Look for size keywords
            size_match = re.search(r'\b(small|medium|large|extra large|xl|l|m|s)\b', description.lower())
            if size_match:
                size = size_match.group(1)
                if size in ['s', 'm', 'l']:
                    size_map = {'s': 'small', 'm': 'medium', 'l': 'large'}
                    size = size_map[size]
                elif size == 'xl':
                    size = 'extra large'
                result[field_name] = size
        
        elif field_name == 'toppings':
            toppings = []
            # Common toppings to look for
            topping_patterns = [
                r'\bpepperoni\b',
                r'\bsausage\b',
                r'\bmushrooms?\b',
                r'\bolives?\b',
                r'\bpeppers?\b',
                r'\bonions?\b',
                r'\bextra cheese\b',
                r'\bcheese\b',
                r'\bham\b',
                r'\bpineapple\b',
                r'\bbeef\b',
                r'\bchicken\b'
            ]
            
            for pattern in topping_patterns:
                if re.search(pattern, description.lower()):
                    topping = re.search(pattern, description.lower()).group(0)
                    if topping not in toppings:
                        toppings.append(topping)
            
            result[field_name] = toppings
        
        elif field_name == 'delivery_address':
            # Look for address patterns
            address_match = re.search(r'\b(\d+\s+[A-Za-z\s]+(?:St|Street|Ave|Avenue|Rd|Road|Blvd|Boulevard|Dr|Drive|Ln|Lane)\.?)\b', description)
            if address_match:
                result[field_name] = address_match.group(1)
        
        elif field_name == 'delivery_time':
            # Look for time patterns
            time_match = re.search(r'\b(\d{1,2}(?::\d{2})?\s*(?:am|pm|AM|PM)|\d{1,2}(?:am|pm|AM|PM))\b', description)
            if time_match:
                result[field_name] = time_match.group(1)

    return result

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())
description = input_data['description']
target_schema = input_data['target_schema']

# Extract structured data
extracted_data = extract_data_from_description(description, target_schema)

# Output as JSON
print(json.dumps(extracted_data, separators=(',', ':')))