import sys

# Read the board
board = []
for _ in range(6):
    line = input().strip()
    board.append(list(line))

# Read the column number
column = int(input().strip())

# Check if column is valid (0-6)
if column < 0 or column > 6:
    print("Invalid")
else:
    # Find the lowest empty row in the specified column
    valid_row = -1
    for row in range(5, -1, -1):  # Start from bottom row (5) and go up
        if board[row][column] == '.':
            valid_row = row
            break
    
    if valid_row == -1:
        print("Invalid")
    else:
        print(f"Valid row {valid_row}")