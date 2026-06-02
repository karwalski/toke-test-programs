import sys
import json
import re

def extract_triples(text):
    triples = []
    
    # Split text into sentences
    sentences = re.split(r'[.!?]+', text.strip())
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        # Pattern 1: Subject founded Object in Year
        match = re.search(r'(.+?)\s+founded\s+(.+?)\s+in\s+(\d+)', sentence)
        if match:
            subject = match.group(1).strip()
            object1 = match.group(2).strip()
            year = match.group(3).strip()
            triples.append({"subject": subject, "predicate": "founded", "object": object1})
            triples.append({"subject": object1, "predicate": "founded_in", "object": year})
            continue
            
        # Pattern 2: Subject is headquartered in Location
        match = re.search(r'(.+?)\s+is\s+headquartered\s+in\s+(.+)', sentence)
        if match:
            subject = match.group(1).strip()
            location = match.group(2).strip()
            triples.append({"subject": subject, "predicate": "headquartered_in", "object": location})
            continue
    
    return triples

# Read input from stdin
text = sys.stdin.read().strip()

# Extract triples
triples = extract_triples(text)

# Output as JSON
print(json.dumps(triples, separators=(',', ':')))