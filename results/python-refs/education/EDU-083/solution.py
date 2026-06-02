import json
import sys
import csv
from io import StringIO

# Read JSON input from stdin
input_data = sys.stdin.read().strip()
quiz_data = json.loads(input_data)

# Create CSV output
output = StringIO()
writer = csv.writer(output)

# Write header
writer.writerow(['student', 'total_correct', 'total_questions', 'percentage'])

# Process each student's results
for student_data in quiz_data:
    student = student_data['student']
    answers = student_data['answers']
    
    total_questions = len(answers)
    total_correct = sum(1 for answer in answers if answer['correct'])
    percentage = round((total_correct / total_questions) * 100) if total_questions > 0 else 0
    
    writer.writerow([student, total_correct, total_questions, f'{percentage}%'])

# Print CSV to stdout
print(output.getvalue().strip())