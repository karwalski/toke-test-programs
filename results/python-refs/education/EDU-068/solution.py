import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())
students = input_data["students"]
topics = input_data["topics"]

# Calculate how many students per topic for expert groups
students_per_topic = len(students) // len(topics)

# Assign students to expert groups
expert_groups = {}
student_idx = 0

for topic in topics:
    expert_groups[topic] = []
    for i in range(students_per_topic):
        expert_groups[topic].append(students[student_idx])
        student_idx += 1

# Print expert groups
print("Expert Groups:")
for topic in topics:
    print(f"{topic}: {', '.join(expert_groups[topic])}")

# Create jigsaw groups
print("Jigsaw Groups:")
for i in range(students_per_topic):
    group_members = []
    for topic in topics:
        student = expert_groups[topic][i]
        group_members.append(f"{student} ({topic})")
    print(f"Group {i + 1}: {', '.join(group_members)}")