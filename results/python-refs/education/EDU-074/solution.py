import json
import sys

# Read input from stdin
input_data = sys.stdin.read().strip()
questions = json.loads(input_data)

# Process each question
for i, q in enumerate(questions, 1):
    # Print question header with time limit
    print(f"Q{i}: {q['question']} ({q['time_limit_sec']}s)")
    
    # Print options A-D
    option_labels = ['A', 'B', 'C', 'D']
    for j, option in enumerate(q['options']):
        print(f"{option_labels[j]}: {option}")
    
    # Print answer
    correct_index = q['correct']
    print(f"Answer: {option_labels[correct_index]}")
    
    # Add blank line between questions (except after the last one)
    if i < len(questions):
        print()