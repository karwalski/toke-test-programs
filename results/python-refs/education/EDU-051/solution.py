import sys
import json

def parse_outline():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    flashcards = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
            
        # Check if this is a top-level item (no indentation)
        if not line.startswith(' ') and not line.startswith('\t'):
            topic = line.strip()
            details = []
            i += 1
            
            # Collect all indented details for this topic
            while i < len(lines):
                if lines[i].strip() == '':
                    i += 1
                    continue
                if lines[i].startswith(' ') or lines[i].startswith('\t'):
                    details.append(lines[i].strip())
                    i += 1
                else:
                    break
            
            # Create flashcard if we have details
            if details:
                front = f"What is {topic}?"
                back = ". ".join(details) + "."
                flashcards.append({"front": front, "back": back})
        else:
            i += 1
    
    return flashcards

flashcards = parse_outline()
print(json.dumps(flashcards, separators=(',', ':')))