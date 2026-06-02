import sys

def read_board():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    return lines

def check_red_win(board):
    n = len(board)
    if n == 0:
        return False
    
    # Start from top edge (row 0) and try to reach bottom edge (row n-1)
    visited = set()
    
    def dfs(row, col):
        if row < 0 or row >= n or col < 0 or col >= len(board[row]):
            return False
        if (row, col) in visited:
            return False
        if board[row][col] != 'R':
            return False
        
        visited.add((row, col))
        
        # If we reached the bottom edge, Red wins
        if row == n - 1:
            return True
        
        # Check all 6 hex neighbors
        # In a typical hex grid representation, neighbors are:
        # (row-1, col-1), (row-1, col), (row, col-1), (row, col+1), (row+1, col), (row+1, col+1)
        neighbors = [
            (row-1, col-1), (row-1, col),
            (row, col-1), (row, col+1),
            (row+1, col), (row+1, col+1)
        ]
        
        for nr, nc in neighbors:
            if dfs(nr, nc):
                return True
        
        return False
    
    # Start DFS from any R piece in the top row
    for col in range(len(board[0])):
        if board[0][col] == 'R':
            if dfs(0, col):
                return True
    
    return False

def check_blue_win(board):
    n = len(board)
    if n == 0:
        return False
    
    # Start from left edge (col 0) and try to reach right edge
    visited = set()
    
    def dfs(row, col):
        if row < 0 or row >= n or col < 0 or col >= len(board[row]):
            return False
        if (row, col) in visited:
            return False
        if board[row][col] != 'B':
            return False
        
        visited.add((row, col))
        
        # If we reached the right edge, Blue wins
        if col == len(board[row]) - 1:
            return True
        
        # Check all 6 hex neighbors
        neighbors = [
            (row-1, col-1), (row-1, col),
            (row, col-1), (row, col+1),
            (row+1, col), (row+1, col+1)
        ]
        
        for nr, nc in neighbors:
            if dfs(nr, nc):
                return True
        
        return False
    
    # Start DFS from any B piece in the leftmost column
    for row in range(n):
        if len(board[row]) > 0 and board[row][0] == 'B':
            if dfs(row, 0):
                return True
    
    return False

def main():
    board = read_board()
    
    if check_red_win(board):
        print("R wins")
    elif check_blue_win(board):
        print("B wins")
    else:
        print("No winner")

if __name__ == "__main__":
    main()