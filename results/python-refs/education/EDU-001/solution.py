import json
import sys

# Read JSON quiz definition from stdin
quiz_data = json.loads(input())

correct_answers = 0
total_questions = len(quiz_data["questions"])

# Process each question
for i, question in enumerate(quiz_data["questions"], 1):
    # Display question
    print(f"Q{i}: {question['q']}")
    
    # Display options
    for option in question["options"]:
        print(option)
    
    # Get user answer
    user_answer = input().strip()
    
    # Check if answer is correct
    if user_answer == question["answer"]:
        print("Correct!")
        correct_answers += 1
    else:
        print("Incorrect!")

# Calculate percentage
percentage = round((correct_answers / total_questions) * 100)

# Display final score
print(f"Score: {correct_answers}/{total_questions} ({percentage}%)")