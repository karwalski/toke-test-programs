import random

# Read seed and set random seed
seed = int(input().strip())
random.seed(seed)

# Read student names
students = []
while True:
    try:
        name = input().strip()
        if name:
            students.append(name)
    except EOFError:
        break

# Create a list of authors (same as students)
authors = students.copy()

# Shuffle the authors list to create random assignments
random.shuffle(authors)

# Check if any student would review themselves
# If so, we need to fix the assignment
for i in range(len(students)):
    if students[i] == authors[i]:
        # Find another position to swap with
        for j in range(len(students)):
            if j != i and students[j] != authors[i] and students[i] != authors[j]:
                # Swap positions i and j in authors list
                authors[i], authors[j] = authors[j], authors[i]
                break

# Output the assignments
for i in range(len(students)):
    print(f"{students[i]} -> {authors[i]}")