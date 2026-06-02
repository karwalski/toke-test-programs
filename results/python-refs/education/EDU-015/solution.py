import json
import sys

# Read JSON input from stdin
input_data = sys.stdin.read().strip()
entries = json.loads(input_data)

# Sort entries by author name
entries.sort(key=lambda x: x['author'])

# Format and output each citation in APA format
for entry in entries:
    author = entry['author']
    year = entry['year']
    title = entry['title']
    print(f"{author} ({year}). {title}.")