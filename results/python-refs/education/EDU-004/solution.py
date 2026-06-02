import json
import sys

# Read JSON input
json_line = input().strip()
data = json.loads(json_line)

terms = data['terms']
definitions = data['definitions']

# Create correct mapping (assuming order matches)
correct_mapping = dict(zip(terms, definitions))

# Read answer pairs
answers = {}
for line in sys.stdin:
    line = line.strip()
    if '=' in line:
        term, definition = line.split('=', 1)
        answers[term] = definition

# Check answers and output results
correct_count = 0
total_count = len(answers)

for term, given_definition in answers.items():
    if term in correct_mapping and correct_mapping[term] == given_definition:
        print(f"{term} -> {given_definition}: Correct")
        correct_count += 1
    else:
        correct_def = correct_mapping.get(term, "Unknown")
        print(f"{term} -> {given_definition}: Incorrect")

# Calculate and display score
percentage = int((correct_count / total_count) * 100) if total_count > 0 else 0
print(f"Score: {correct_count}/{total_count} ({percentage}%)")