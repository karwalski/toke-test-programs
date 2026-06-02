import sys
from collections import deque

def read_maze():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    return lines

def find_start_end(maze):
    start = end = None
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == 'S':
                start = (i, j)
            elif maze[i][j] == 'E':
                end = (i, j)
    return start, end

def get_neighbors(pos, maze):
    i, j = pos
    neighbors = []
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    for di, dj in directions:
        ni, nj = i + di, j + dj
        if 0 <= ni < len(maze) and 0 <= nj < len(maze[ni]):
            if maze[ni][nj] != '#':
                neighbors.append((ni, nj))
    return neighbors

def find_solution_length(maze, start, end):
    queue = deque([(start, 0)])
    visited = {start}
    
    while queue:
        pos, dist = queue.popleft()
        if pos == end:
            return dist
        
        for neighbor in get_neighbors(pos, maze):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    
    return -1

def count_decision_points_and_dead_ends(maze, start, end):
    decision_points = 0
    dead_ends = 0
    
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] != '#':
                neighbors = get_neighbors((i, j), maze)
                neighbor_count = len(neighbors)
                
                if neighbor_count >= 3:
                    decision_points += 1
                elif neighbor_count == 1 and (i, j) != start and (i, j) != end:
                    dead_ends += 1
    
    return decision_points, dead_ends

def rate_difficulty(decision_points, dead_ends, solution_length):
    score = decision_points * 2 + dead_ends + solution_length // 10
    
    if score <= 3:
        return "Easy"
    elif score <= 6:
        return "Medium"
    else:
        return "Hard"

def main():
    maze = read_maze()
    start, end = find_start_end(maze)
    
    decision_points, dead_ends = count_decision_points_and_dead_ends(maze, start, end)
    solution_length = find_solution_length(maze, start, end)
    difficulty = rate_difficulty(decision_points, dead_ends, solution_length)
    
    print(f"Decision points: {decision_points}")
    print(f"Dead ends: {dead_ends}")
    print(f"Solution length: {solution_length}")
    print(f"Difficulty: {difficulty}")

if __name__ == "__main__":
    main()