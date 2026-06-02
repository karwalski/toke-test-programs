import json
import sys

# Read input
filter_line = input().strip()
questions_line = input().strip()

# Parse JSON
filter_criteria = json.loads(filter_line)
questions = json.loads(questions_line)

# Filter questions
filtered_questions = []
for question in questions:
    if (question["topic"] == filter_criteria["topic"] and 
        question["difficulty"] == filter_criteria["difficulty"] and 
        question["type"] == filter_criteria["type"]):
        filtered_questions.append(question)

# Output filtered questions
for i, question in enumerate(filtered_questions, 1):
    print(f"{i}. [{question['topic']}, d{question['difficulty']}, {question['type']}] {question['q']}")