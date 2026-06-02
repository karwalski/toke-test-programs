import sys

# Read input
line1 = input().strip()
line2 = input().strip()

# Parse phase
phase = line1

# Parse dice values
dice1, dice2 = map(int, line2.split())
roll_total = dice1 + dice2

if phase == 'comeout':
    # Come-out roll rules
    if roll_total in [7, 11]:
        print("Win")
    elif roll_total in [2, 3, 12]:
        print("Lose")
    else:
        print(f"Point {roll_total}")
else:
    # Point phase - phase contains the point number
    point = int(phase)
    if roll_total == point:
        print("Win")
    elif roll_total == 7:
        print("Lose")
    else:
        print(f"Point {point}")