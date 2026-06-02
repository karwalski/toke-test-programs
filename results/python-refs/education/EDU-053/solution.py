import json
import sys

# Read JSON input from stdin
input_data = json.load(sys.stdin)

passage = input_data["passage"]
questions = input_data["questions"]
student_answers = input_data["student_answers"]

# Score each question
correct_count = 0
total_questions = len(questions)

for i in range(total_questions):
    question_num = i + 1
    correct_answer = questions[i]["answer"].strip().lower()
    student_answer = student_answers[i].strip().lower() if i < len(student_answers) else ""
    
    if student_answer == correct_answer:
        print(f"Q{question_num}: Correct")
        correct_count += 1
    else:
        print(f"Q{question_num}: Incorrect")

# Calculate and display overall score
percentage = round((correct_count / total_questions) * 100) if total_questions > 0 else 0
print(f"Score: {correct_count}/{total_questions} ({percentage}%)")