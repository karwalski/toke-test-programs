import json
import sys

# Read the JSON array from first line
questions_data = json.loads(input().strip())

# Read answers for each question
user_answers = []
for _ in range(len(questions_data)):
    user_answers.append(input().strip())

# Check answers and output results
correct_count = 0
for i, (question_obj, user_answer) in enumerate(zip(questions_data, user_answers), 1):
    correct_answer = question_obj["answer"]
    if user_answer == correct_answer:
        print(f"Q{i}: Correct")
        correct_count += 1
    else:
        print(f"Q{i}: Incorrect")

# Calculate and output final score
total_questions = len(questions_data)
percentage = int((correct_count / total_questions) * 100)
print(f"Score: {correct_count}/{total_questions} ({percentage}%)")