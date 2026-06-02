import sys
import re

for line in sys.stdin:
    title = line.strip()
    if title:
        # Convert to lowercase
        slug = title.lower()
        # Replace non-alphanumeric characters with hyphens
        slug = re.sub(r'[^a-z0-9]+', '-', slug)
        # Remove leading and trailing hyphens
        slug = slug.strip('-')
        print(slug)