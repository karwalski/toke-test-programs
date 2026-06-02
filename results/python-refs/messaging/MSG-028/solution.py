import json
import sys
import re

# Read the first line containing banned keywords/patterns
banned_keywords = json.loads(input().strip())

# Process each message
for line in sys.stdin:
    message = line.strip()
    if not message:
        continue
    
    matched_keywords = []
    message_lower = message.lower()
    
    # Check each banned keyword/pattern
    for keyword in banned_keywords:
        keyword_lower = keyword.lower()
        if keyword_lower in message_lower:
            matched_keywords.append(keyword)
    
    # Output result
    if matched_keywords:
        print(f"SPAM [{', '.join(matched_keywords)}]")
    else:
        print("HAM")