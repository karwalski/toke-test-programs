import json
import sys
import random

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

students = input_data["students"]
motion = input_data["motion"]
seed = input_data["seed"]

# Set the random seed for reproducible results
random.seed(seed)

# Shuffle the students list
shuffled_students = students.copy()
random.shuffle(shuffled_students)

# Split students into two teams
mid_point = len(shuffled_students) // 2
for_team = shuffled_students[:mid_point]
against_team = shuffled_students[mid_point:]

# If odd number of students, add the extra to FOR team
if len(shuffled_students) % 2 == 1:
    for_team.append(against_team.pop())

# Sort teams alphabetically for consistent output
for_team.sort()
against_team.sort()

# Print output in exact format
print(f"Motion: {motion}")
print(f"FOR: {', '.join(for_team)}")
print(f"AGAINST: {', '.join(against_team)}")