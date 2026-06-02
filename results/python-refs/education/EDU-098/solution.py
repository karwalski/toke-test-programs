import json
import sys

# Read input from stdin
input_data = sys.stdin.read().strip()

# Parse JSON
glossary = json.loads(input_data)

# Sort by term alphabetically
glossary.sort(key=lambda x: x['term'])

# Format and print output
for i, entry in enumerate(glossary):
    print(entry['term'])
    print(f"  {entry['definition']}")
    if i < len(glossary) - 1:
        print()