def solve_sudoku(board):
    def is_valid(board, row, col, num):
        # Check row
        for j in range(9):
            if board[row][j] == num:
                return False
        
        # Check column
        for i in range(9):
            if board[i][col] == num:
                return False
        
        # Check 3x3 box
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i][j] == num:
                    return False
        
        return True
    
    def backtrack(board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    for num in range(1, 10):
                        if is_valid(board, i, j, num):
                            board[i][j] = num
                            if backtrack(board):
                                return True
                            board[i][j] = 0
                    return False
        return True
    
    backtrack(board)
    return board

# Read input
board = []
for _ in range(9):
    line = input().strip()
    row = []
    for char in line:
        if char == '.':
            row.append(0)
        else:
            row.append(int(char))
    board.append(row)

# Solve the puzzle
solution = solve_sudoku(board)

# Output the solution
for row in solution:
    print(''.join(map(str, row)))