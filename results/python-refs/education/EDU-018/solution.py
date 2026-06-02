import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

rubric = input_data["criteria"]
scores = input_data["scores"]

total_score = 0
total_max = 0

# Print individual criterion scores
for criterion in rubric:
    name = criterion["name"]
    max_score = criterion["max_score"]
    score = scores[name]
    
    print(f"{name}: {score}/{max_score}")
    
    total_score += score
    total_max += max_score

# Calculate percentage
percentage = round(total_score * 100 / total_max)

# Print total
print(f"Total: {total_score}/{total_max} ({percentage}%)")