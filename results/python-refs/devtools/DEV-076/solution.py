import json
import sys

# Read JSON from stdin
input_data = sys.stdin.read().strip()
checklist = json.loads(input_data)

# Find incomplete required items
incomplete_required = []
for item in checklist:
    if item["required"] and not item["completed"]:
        incomplete_required.append(item["item"])

# Output result
if not incomplete_required:
    print("RELEASE READY")
else:
    print("BLOCKED")
    print("Incomplete required items:")
    for item in incomplete_required:
        print(f"- {item}")