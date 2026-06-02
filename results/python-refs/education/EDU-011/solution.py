import json
import sys

# Read all input
input_lines = []
for line in sys.stdin:
    input_lines.append(line.rstrip('\n'))

# Find the QUIZ marker
quiz_index = input_lines.index('QUIZ')

# Parse the JSON vocabulary list
vocab_json = '\n'.join(input_lines[:quiz_index])
vocab_list = json.loads(vocab_json)

# Create a dictionary for quick lookup
vocab_dict = {item['word']: item['definition'] for item in vocab_list}

# Get quiz words and answers
quiz_data = input_lines[quiz_index + 1:]
quiz_words = []
quiz_answers = []

for i in range(0, len(quiz_data), 2):
    quiz_words.append(quiz_data[i])
    if i + 1 < len(quiz_data):
        quiz_answers.append(quiz_data[i + 1])

# Process quiz
correct_count = 0
total_questions = len(quiz_words)

for i, word in enumerate(quiz_words):
    print(f"Define: {word}")
    
    if i < len(quiz_answers):
        user_answer = quiz_answers[i]
        correct_definition = vocab_dict.get(word, "")
        
        if user_answer.strip().lower() == correct_definition.strip().lower():
            print("Correct!")
            correct_count += 1
        else:
            print("Incorrect!")

# Calculate and display score
if total_questions > 0:
    percentage = int((correct_count / total_questions) * 100)
    print(f"Score: {correct_count}/{total_questions} ({percentage}%)")