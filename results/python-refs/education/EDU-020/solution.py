import json
import sys

# Read input from stdin
input_data = sys.stdin.read().strip()

# Parse JSON
assignments = json.loads(input_data)

# Sort by due date
assignments.sort(key=lambda x: x['due_date'])

# Output each assignment
for assignment in assignments:
    checkbox = '[x]' if assignment['completed'] else '[ ]'
    print(f"{checkbox} {assignment['due_date']} {assignment['title']}")