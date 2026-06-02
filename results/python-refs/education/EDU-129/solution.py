import json
import sys

# Read input from stdin
input_data = sys.stdin.read().strip()
students = json.loads(input_data)

# Process each student
for student_data in students:
    name = student_data["student"]
    scores = student_data["quiz_scores"]
    
    # Calculate average score
    avg_score = sum(scores) / len(scores)
    
    # Determine comprehension level based on average
    if avg_score >= 80:
        level = "Mastery"
    elif avg_score >= 65:
        level = "Developing"
    else:
        level = "Beginning"
    
    # Output in required format
    print(f"{name}: {level} ({avg_score})")