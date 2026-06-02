import json
import sys

# Read the first line as JSON tag dictionary
tag_dict_line = input().strip()
tag_dict = json.loads(tag_dict_line)

# Process remaining lines
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    matched_tags = []
    
    # Check each tag and its keywords
    for tag, keywords in tag_dict.items():
        for keyword in keywords:
            if keyword.lower() in line.lower():
                if tag not in matched_tags:
                    matched_tags.append(tag)
                break
    
    # Output the line with tags
    if matched_tags:
        print(f"{line} [{', '.join(matched_tags)}]")
    else:
        print(line)