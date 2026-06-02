import sys
import json
import random

# Read input
line1 = input().strip()
line2 = input().strip()

# Parse first line
seed, num_questions = map(int, line1.split())

# Parse JSON array
questions = json.loads(line2)

# Set random seed for reproducible results
random.seed(seed)

# Generate random subset
selected_questions = random.sample(questions, num_questions)

# Output numbered questions
for i, question in enumerate(selected_questions, 1):
    print(f"{i}. {question['q']}")