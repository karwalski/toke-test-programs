import json
import re
import sys
from datetime import datetime

def extract_fields(text, schema):
    result = {}
    
    for field, field_type in schema.items():
        if field == "name":
            # Look for "I am [Name]" pattern
            name_match = re.search(r'I am ([A-Za-z\s]+?)(?:,|\.|\s+I\s|\s+and\s)', text)
            if name_match:
                result[field] = name_match.group(1).strip()
            else:
                result[field] = None
                
        elif field == "address":
            # Look for "live at [address]" pattern
            address_match = re.search(r'live at (.+?)(?:\s+and\s|\s+,\s*and\s)', text)
            if address_match:
                result[field] = address_match.group(1).strip()
            else:
                result[field] = None
                
        elif field == "phone":
            # Look for phone number patterns
            phone_match = re.search(r'phone is (\d{4}-\d{3}-\d{3})', text)
            if phone_match:
                result[field] = phone_match.group(1)
            else:
                result[field] = None
                
        elif field == "date_of_birth":
            # Look for date patterns like "March 5, 1990"
            date_match = re.search(r'born on ([A-Za-z]+ \d{1,2}, \d{4})', text)
            if date_match:
                date_str = date_match.group(1)
                try:
                    # Parse and convert to YYYY-MM-DD format
                    parsed_date = datetime.strptime(date_str, '%B %d, %Y')
                    result[field] = parsed_date.strftime('%Y-%m-%d')
                except:
                    result[field] = None
            else:
                result[field] = None
        else:
            result[field] = None
    
    return result

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())
text = input_data["text"]
schema = input_data["schema"]

# Extract fields
output = extract_fields(text, schema)

# Write output to stdout
print(json.dumps(output, separators=(',', ':')))