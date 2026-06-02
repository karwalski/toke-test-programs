import json
import sys
import re

# Read input
query_line = input().strip()
json_line = input().strip()

# Parse input
keywords = query_line.split()
messages = json.loads(json_line)

# Convert keywords to lowercase for case-insensitive matching
keywords_lower = [kw.lower() for kw in keywords]

matching_messages = []

for message in messages:
    text = message['text']
    text_lower = text.lower()
    
    # Check if any keyword appears in the message
    has_match = False
    for keyword in keywords_lower:
        if keyword in text_lower:
            has_match = True
            break
    
    if has_match:
        # Highlight keywords in the text
        highlighted_text = text
        for keyword in keywords_lower:
            # Create a case-insensitive regex pattern
            pattern = re.compile(re.escape(keyword), re.IGNORECASE)
            highlighted_text = pattern.sub(f'**{keyword.title()}**', highlighted_text)
        
        matching_messages.append({
            'id': message['id'],
            'sender': message['sender'],
            'text': highlighted_text,
            'time': message['time']
        })

# Output results
for msg in matching_messages:
    print(f"[{msg['id']}] {msg['sender']} ({msg['time']}): {msg['text']}")

print(f"{len(matching_messages)} matches found")