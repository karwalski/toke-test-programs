import json
import sys

# Read JSON input
json_input = input().strip()
questions = json.loads(json_input)

# Read answers
answers = []
for _ in range(len(questions)):
    answers.append(input().strip())

# Process each question
correct_count = 0
total_count = len(questions)

for i, question in enumerate(questions):
    sentence = question["sentence"]
    correct_answer = question["answer"]
    user_answer = answers[i]
    
    # Print the sentence
    print(sentence)
    
    # Check if answer is correct (case-insensitive)
    if user_answer.lower() == correct_answer.lower():
        print("Correct")
        correct_count += 1
    else:
        print("Incorrect")

# Calculate and print final score
percentage = round((correct_count / total_count) * 100)
print(f"Score: {correct_count}/{total_count} ({percentage}%)")