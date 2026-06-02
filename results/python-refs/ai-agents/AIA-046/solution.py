import sys
import json
import re

def extract_entities(text):
    entities = []
    
    # Person pattern: capitalized words (first and last name)
    person_pattern = r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b'
    for match in re.finditer(person_pattern, text):
        entities.append({
            "text": match.group(),
            "type": "person",
            "start_offset": match.start(),
            "end_offset": match.end()
        })
    
    # Organization pattern: Microsoft, Apple, etc. (capitalized single words after "from")
    org_pattern = r'(?:from\s+)([A-Z][a-z]+)'
    for match in re.finditer(org_pattern, text):
        entities.append({
            "text": match.group(1),
            "type": "organization", 
            "start_offset": match.start(1),
            "end_offset": match.end(1)
        })
    
    # Location pattern: capitalized single words after "visited"
    location_pattern = r'(?:visited\s+)([A-Z][a-z]+)'
    for match in re.finditer(location_pattern, text):
        entities.append({
            "text": match.group(1),
            "type": "location",
            "start_offset": match.start(1), 
            "end_offset": match.end(1)
        })
    
    # Date pattern: Month Day, Year format
    date_pattern = r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(?:st|nd|rd|th)?,\s+\d{4}\b'
    for match in re.finditer(date_pattern, text):
        entities.append({
            "text": match.group(),
            "type": "date",
            "start_offset": match.start(),
            "end_offset": match.end()
        })
    
    # Sort by start_offset to maintain order
    entities.sort(key=lambda x: x['start_offset'])
    
    return entities

# Read input from stdin
text = sys.stdin.read().strip()

# Extract entities
entities = extract_entities(text)

# Output JSON
print(json.dumps(entities, separators=(',', ':')))