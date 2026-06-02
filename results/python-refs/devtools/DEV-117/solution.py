import json
import sys
from datetime import datetime

def parse_filter(filter_str):
    if filter_str == 'all':
        return 'all', None
    elif filter_str.startswith('tag:'):
        return 'tag', filter_str[4:]
    elif filter_str.startswith('before:'):
        return 'before', filter_str[7:]
    else:
        return 'unknown', None

def short_digest(digest):
    if digest.startswith('sha256:'):
        return digest[:10]
    return digest[:7]

def filter_images(images, filter_type, filter_value):
    filtered = []
    
    for image in images:
        if filter_type == 'all':
            filtered.append(image)
        elif filter_type == 'tag':
            if image['tag'] == filter_value:
                filtered.append(image)
        elif filter_type == 'before':
            image_date = datetime.strptime(image['pushed'], '%Y-%m-%d')
            filter_date = datetime.strptime(filter_value, '%Y-%m-%d')
            if image_date < filter_date:
                filtered.append(image)
    
    return filtered

# Read input
filter_str = input().strip()
json_str = input().strip()

# Parse filter
filter_type, filter_value = parse_filter(filter_str)

# Parse JSON
images = json.loads(json_str)

# Filter images
filtered_images = filter_images(images, filter_type, filter_value)

# Output results
for image in filtered_images:
    digest_short = short_digest(image['digest'])
    print(f"{image['repo']}:{image['tag']} ({digest_short}) {image['pushed']}")