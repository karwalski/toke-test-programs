from collections import deque
import sys

def solve_maze():
    # Read maze from stdin
    maze_lines = []
    for line in sys.stdin:
        maze_lines.append(list(line.rstrip('\n')))
    
    if not maze_lines:
        print("No solution")
        return
    
    rows = len(maze_lines)
    cols = len(maze_lines[0]) if rows > 0 else 0
    
    # Find start and end positions
    start = None
    end = None
    for i in range(rows):
        for j in range(cols):
            if maze_lines[i][j] == 'S':
                start = (i, j)
            elif maze_lines[i][j] == 'E':
                end = (i, j)
    
    if start is None or end is None:
        print("No solution")
        return
    
    # BFS to find path
    queue = deque([(start, [start])])
    visited = {start}
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    while queue:
        (row, col), path = queue.popleft()
        
        if (row, col) == end:
            # Found solution, mark path
            for r, c in path[1:-1]:  # Skip start and end positions
                maze_lines[r][c] = '*'
            
            # Print the maze
            for line in maze_lines:
                print(''.join(line))
            return
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            if (0 <= new_row < rows and 
                0 <= new_col < cols and 
                (new_row, new_col) not in visited and
                maze_lines[new_row][new_col] in [' ', 'E']):
                
                visited.add((new_row, new_col))
                queue.append(((new_row, new_col), path + [(new_row, new_col)]))
    
    print("No solution")

solve_maze()