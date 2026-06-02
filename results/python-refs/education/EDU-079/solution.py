import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

threshold = input_data["threshold"]
students = input_data["students"]

for student_data in students:
    name = student_data["student"]
    assessments = student_data["assessments"]
    
    # Calculate average
    average = sum(assessments) / len(assessments)
    
    # Determine status
    if average >= threshold:
        status = "ON TRACK"
    else:
        status = "NEEDS SUPPORT"
    
    # Print result
    print(f"{name}: {average:.1f} - {status}")