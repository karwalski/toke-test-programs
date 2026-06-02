import json
import random

# Read input
line1 = input().strip().split()
seed = int(line1[0])
num_questions = int(line1[1])
question_bank_json = input().strip()

# Parse question bank
question_bank = json.loads(question_bank_json)

# Set random seed
random.seed(seed)

# Randomly select N questions
selected_questions = random.sample(question_bank, num_questions)

# Output selected questions numbered and formatted
for i, question in enumerate(selected_questions, 1):
    print(f"{i}. [{question['topic']}] {question['q']}")