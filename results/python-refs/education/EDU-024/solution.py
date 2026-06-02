import random
import sys

# Read input
lines = sys.stdin.read().strip().split('\n')
seed = int(lines[0])
group_size = int(lines[1])
students = lines[2:]

# Set random seed
random.seed(seed)

# Shuffle students
random.shuffle(students)

# Create groups
group_num = 1
for i in range(0, len(students), group_size):
    group = students[i:i + group_size]
    print(f"Group {group_num}: {', '.join(group)}")
    group_num += 1