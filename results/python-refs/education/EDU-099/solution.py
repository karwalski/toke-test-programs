import json
import sys

# Read JSON input from stdin
input_data = json.loads(sys.stdin.read().strip())

answer_key = input_data["answer_key"]
student_responses = input_data["student_responses"]

correct_count = 0
total_questions = len(answer_key)

# Process each question
for i in range(total_questions):
    question_num = i + 1
    student_answer = student_responses[i]
    correct_answer = answer_key[i]
    
    if student_answer == correct_answer:
        print(f"Q{question_num}: {student_answer} (correct)")
        correct_count += 1
    else:
        print(f"Q{question_num}: {student_answer} (incorrect, answer: {correct_answer})")

# Calculate and display score
percentage = round((correct_count / total_questions) * 100)
print(f"Score: {correct_count}/{total_questions} ({percentage}%)")