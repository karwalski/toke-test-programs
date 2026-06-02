import json
import sys

# Read JSON input from stdin
input_data = json.loads(sys.stdin.read())

# Extract data
version = input_data["version"]
date = input_data["date"]
changes = input_data["changes"]

# Generate markdown output
print(f"# Release {version} ({date})")
print()

for change in changes:
    category = change["category"]
    items = change["items"]
    
    print(f"## {category}")
    for item in items:
        print(f"- {item}")
    print()