import json
import sys

# Read input from stdin
input_data = sys.stdin.read().strip()

# Parse JSON
students = json.loads(input_data)

# Sort students by ID
students.sort(key=lambda student: student["id"])

# Output sorted roster
for i, student in enumerate(students, 1):
    print(f"{i}. ID: {student['id']} | Name: {student['name']} | Grade: {student['grade']}")