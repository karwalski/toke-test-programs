import json
import sys

# Read input from stdin
input_data = sys.stdin.read().strip()
students = json.loads(input_data)

# Process each student and calculate attendance
results = []
for student in students:
    name = student["name"]
    records = student["records"]
    
    total = len(records)
    present = records.count('P')
    percentage = (present * 100) // total
    
    results.append((name, percentage, present, total))

# Sort by name
results.sort(key=lambda x: x[0])

# Output results
for name, percentage, present, total in results:
    print(f"{name}: {percentage}% ({present} present / {total} total)")