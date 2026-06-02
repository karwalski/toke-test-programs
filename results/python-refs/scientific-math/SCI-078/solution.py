def is_safe(board, row, col, n):
    # Check column
    for i in range(row):
        if board[i] == col:
            return False
    
    # Check diagonal (top-left to bottom-right)
    for i in range(row):
        if abs(board[i] - col) == abs(i - row):
            return False
    
    return True

def solve_nqueens(board, row, n, solutions):
    if row == n:
        solutions.append(board[:])
        return
    
    for col in range(1, n + 1):
        if is_safe(board, row, col, n):
            board[row] = col
            solve_nqueens(board, row + 1, n, solutions)

def main():
    n = int(input())
    board = [0] * n
    solutions = []
    
    solve_nqueens(board, 0, n, solutions)
    
    for i, solution in enumerate(solutions, 1):
        print(f"Solution {i}: {' '.join(map(str, solution))}")
    
    print(f"Total solutions: {len(solutions)}")

if __name__ == "__main__":
    main()