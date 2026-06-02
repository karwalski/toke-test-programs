def is_safe(board, row, col, n):
    # Check column
    for i in range(row):
        if board[i] == col:
            return False
    
    # Check diagonals
    for i in range(row):
        if abs(board[i] - col) == abs(i - row):
            return False
    
    return True

def solve_nqueens(board, row, n, solutions):
    if row == n:
        solutions.append(board[:])
        return
    
    for col in range(n):
        if is_safe(board, row, col, n):
            board[row] = col
            solve_nqueens(board, row + 1, n, solutions)

def nqueens(n):
    solutions = []
    board = [-1] * n
    solve_nqueens(board, 0, n, solutions)
    return solutions

n = int(input())
solutions = nqueens(n)

print(len(solutions))
for solution in solutions:
    print(' '.join(str(pos + 1) for pos in solution))