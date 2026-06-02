import random
import sys

def generate_maze(width, height, seed):
    random.seed(seed)
    
    # Create grid with all walls (True = wall, False = passage)
    # Grid dimensions are (2*height + 1) x (2*width + 1) to include walls
    grid_height = 2 * height + 1
    grid_width = 2 * width + 1
    grid = [[True for _ in range(grid_width)] for _ in range(grid_height)]
    
    # Stack for backtracking
    stack = []
    
    # Start at top-left cell (1,1)
    start_row, start_col = 1, 1
    grid[start_row][start_col] = False  # Mark as passage
    stack.append((start_row, start_col))
    
    # Directions: up, right, down, left
    directions = [(-2, 0), (0, 2), (2, 0), (0, -2)]
    
    while stack:
        current_row, current_col = stack[-1]
        
        # Find unvisited neighbors
        neighbors = []
        for dr, dc in directions:
            new_row, new_col = current_row + dr, current_col + dc
            # Check bounds and if cell is unvisited (still a wall)
            if (1 <= new_row < grid_height - 1 and 
                1 <= new_col < grid_width - 1 and 
                grid[new_row][new_col]):
                neighbors.append((new_row, new_col, dr, dc))
        
        if neighbors:
            # Choose random neighbor
            new_row, new_col, dr, dc = random.choice(neighbors)
            
            # Remove wall between current cell and chosen neighbor
            wall_row = current_row + dr // 2
            wall_col = current_col + dc // 2
            grid[wall_row][wall_col] = False
            
            # Mark new cell as passage and add to stack
            grid[new_row][new_col] = False
            stack.append((new_row, new_col))
        else:
            # Backtrack
            stack.pop()
    
    return grid

def print_maze(grid):
    for row in grid:
        line = ""
        for cell in row:
            line += "#" if cell else " "
        print(line)

# Read input
line = input().strip()
width, height, seed = map(int, line.split())

# Generate and print maze
maze = generate_maze(width, height, seed)
print_maze(maze)