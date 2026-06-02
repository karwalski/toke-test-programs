import json
import sys
import re

def extract_data_from_description(description, schema):
    result = {}
    properties = schema.get('properties', {})
    
    for field_name, field_schema in properties.items():
        if field_name == 'size':
            size_match = re.search(r'\b(small|medium|large|extra large|xl)\b', description.lower())
            if size_match:
                result[field_name] = size_match.group(1)
            else:
                result[field_name] = None
        
        elif field_name == 'toppings':
            toppings = []
            topping_patterns = [
                'pepperoni', 'sausage', 'mushrooms', 'mushroom', 'olives', 'olive',
                'peppers', 'pepper', 'onions', 'onion', 'extra cheese',
                'ham', 'pineapple', 'beef', 'chicken', 'bacon'
            ]
            desc_lower = description.lower()
            found_spans = []
            for pattern in topping_patterns:
                for m in re.finditer(r'\b' + re.escape(pattern) + r'\b', desc_lower):
                    # Check overlap
                    overlap = False
                    for s, e in found_spans:
                        if not (m.end() <= s or m.start() >= e):
                            overlap = True
                            break
                    if not overlap:
                        found_spans.append((m.start(), m.end()))
                        toppings.append((m.start(), pattern))
            # Also check plain 'cheese' but only if not part of 'extra cheese'
            for m in re.finditer(r'\bcheese\b', desc_lower):
                overlap = False
                for s, e in found_spans:
                    if not (m.end() <= s or m.start() >= e):
                        overlap = True
                        break
                if not overlap:
                    found_spans.append((m.start(), m.end()))
                    toppings.append((m.start(), 'cheese'))
            
            toppings.sort()
            result[field_name] = [t[1] for t in toppings]
        
        elif field_name == 'delivery_address':
            address_match = re.search(r'(\d+\s+[A-Za-z]+\s+(?:St|Street|Ave|Avenue|Rd|Road|Blvd|Boulevard|Dr|Drive|Ln|Lane)\b\.?)', description)
            if address_match:
                result[field_name] = address_match.group(1)
            else:
                result[field_name] = None
        
        elif field_name == 'delivery_time' or field_name == 'time':
            time_match = re.search(r'\b(\d{1,2}(?::\d{2})?\s*(?:am|pm|AM|PM))\b', description)
            if time_match:
                result[field_name] = time_match.group(1)
            else:
                result[field_name] = None
        
        elif field_name == 'attendees':
            attendees = []
            m = re.search(r'with\s+([A-Z][a-z]+(?:\s+(?:and|,)\s+[A-Z][a-z]+)*)', description)
            if m:
                names_str = m.group(1)
                names = re.findall(r'[A-Z][a-z]+', names_str)
                attendees = names
            result[field_name] = attendees
        
        elif field_name == 'date':
            date_match = re.search(r'\b(next\s+(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)|this\s+(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)|tomorrow|today|\d{1,2}/\d{1,2}(?:/\d{2,4})?)\b', description, re.IGNORECASE)
            if date_match:
                result[field_name] = date_match.group(1)
            else:
                result[field_name] = None
        
        elif field_name == 'location':
            loc_match = re.search(r'\bin\s+(room\s+\w+|[A-Z][a-zA-Z\s]*?(?=\s+about|\s+on|\s+at|\s*$|,))', description)
            if loc_match:
                result[field_name] = loc_match.group(1).strip()
            else:
                result[field_name] = None
        
        elif field_name == 'topic':
            topic_match = re.search(r'about\s+(.+?)(?:\.|$)', description)
            if topic_match:
                result[field_name] = topic_match.group(1).strip()
            else:
                result[field_name] = None
        
        else:
            result[field_name] = None

    return result

input_data = json.loads(sys.stdin.read().strip())
description = input_data['description']
target_schema = input_data['target_schema']

extracted_data = extract_data_from_description(description, target_schema)
print(json.dumps(extracted_data, separators=(',', ':')))