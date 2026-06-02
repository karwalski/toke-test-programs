def solve_skyscraper():
    n = int(input())
    top_clues = list(map(int, input().split()))
    bottom_clues = list(map(int, input().split()))
    left_clues = list(map(int, input().split()))
    right_clues = list(map(int, input().split()))
    
    # Initialize grid
    grid = [[0 for _ in range(n)] for _ in range(n)]
    
    def is_valid_placement(grid, row, col, height):
        # Check if height already exists in row
        for c in range(n):
            if c != col and grid[row][c] == height:
                return False
        
        # Check if height already exists in column
        for r in range(n):
            if r != row and grid[r][col] == height:
                return False
        
        return True
    
    def count_visible(line):
        count = 0
        max_height = 0
        for height in line:
            if height > max_height:
                count += 1
                max_height = height
        return count
    
    def check_clues(grid):
        # Check all clues
        for i in range(n):
            # Check row clues
            if left_clues[i] != 0:
                if count_visible([grid[i][j] for j in range(n)]) != left_clues[i]:
                    return False
            if right_clues[i] != 0:
                if count_visible([grid[i][j] for j in range(n-1, -1, -1)]) != right_clues[i]:
                    return False
            
            # Check column clues
            if top_clues[i] != 0:
                if count_visible([grid[j][i] for j in range(n)]) != top_clues[i]:
                    return False
            if bottom_clues[i] != 0:
                if count_visible([grid[j][i] for j in range(n-1, -1, -1)]) != bottom_clues[i]:
                    return False
        
        return True
    
    def is_partial_valid(grid, row, col):
        # Check partial constraints for current position
        # Check row constraint if row is complete
        if col == n - 1:  # Last column, check row clues
            if left_clues[row] != 0:
                if count_visible([grid[row][j] for j in range(n)]) != left_clues[row]:
                    return False
            if right_clues[row] != 0:
                if count_visible([grid[row][j] for j in range(n-1, -1, -1)]) != right_clues[row]:
                    return False
        
        # Check column constraint if column is complete
        if row == n - 1:  # Last row, check column clues
            if top_clues[col] != 0:
                if count_visible([grid[j][col] for j in range(n)]) != top_clues[col]:
                    return False
            if bottom_clues[col] != 0:
                if count_visible([grid[j][col] for j in range(n-1, -1, -1)]) != bottom_clues[col]:
                    return False
        
        return True
    
    def solve(pos):
        if pos == n * n:
            return check_clues(grid)
        
        row = pos // n
        col = pos % n
        
        for height in range(1, n + 1):
            if is_valid_placement(grid, row, col, height):
                grid[row][col] = height
                
                if is_partial_valid(grid, row, col):
                    if solve(pos + 1):
                        return True
                
                grid[row][col] = 0
        
        return False
    
    if solve(0):
        for row in grid:
            print(' '.join(map(str, row)))
    else:
        print("No solution found")

solve_skyscraper()