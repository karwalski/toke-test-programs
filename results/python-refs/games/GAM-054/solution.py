import heapq
from collections import deque

def read_input():
    puzzle = []
    for _ in range(4):
        row = list(map(int, input().split()))
        puzzle.append(row)
    return puzzle

def find_blank(puzzle):
    for i in range(4):
        for j in range(4):
            if puzzle[i][j] == 0:
                return i, j

def get_neighbors(puzzle):
    blank_row, blank_col = find_blank(puzzle)
    neighbors = []
    
    # Up - move tile down to blank
    if blank_row > 0:
        new_puzzle = [row[:] for row in puzzle]
        new_puzzle[blank_row][blank_col] = new_puzzle[blank_row-1][blank_col]
        new_puzzle[blank_row-1][blank_col] = 0
        neighbors.append((new_puzzle, 'U'))
    
    # Down - move tile up to blank
    if blank_row < 3:
        new_puzzle = [row[:] for row in puzzle]
        new_puzzle[blank_row][blank_col] = new_puzzle[blank_row+1][blank_col]
        new_puzzle[blank_row+1][blank_col] = 0
        neighbors.append((new_puzzle, 'D'))
    
    # Left - move tile right to blank
    if blank_col > 0:
        new_puzzle = [row[:] for row in puzzle]
        new_puzzle[blank_row][blank_col] = new_puzzle[blank_row][blank_col-1]
        new_puzzle[blank_row][blank_col-1] = 0
        neighbors.append((new_puzzle, 'L'))
    
    # Right - move tile left to blank
    if blank_col < 3:
        new_puzzle = [row[:] for row in puzzle]
        new_puzzle[blank_row][blank_col] = new_puzzle[blank_row][blank_col+1]
        new_puzzle[blank_row][blank_col+1] = 0
        neighbors.append((new_puzzle, 'R'))
    
    return neighbors

def manhattan_distance(puzzle):
    distance = 0
    for i in range(4):
        for j in range(4):
            if puzzle[i][j] != 0:
                target_row = (puzzle[i][j] - 1) // 4
                target_col = (puzzle[i][j] - 1) % 4
                distance += abs(i - target_row) + abs(j - target_col)
    return distance

def puzzle_to_tuple(puzzle):
    return tuple(tuple(row) for row in puzzle)

def is_goal(puzzle):
    goal = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
    return puzzle == goal

def count_inversions(puzzle):
    flat = []
    for row in puzzle:
        for val in row:
            if val != 0:
                flat.append(val)
    
    inversions = 0
    for i in range(len(flat)):
        for j in range(i + 1, len(flat)):
            if flat[i] > flat[j]:
                inversions += 1
    return inversions

def is_solvable(puzzle):
    inversions = count_inversions(puzzle)
    blank_row, _ = find_blank(puzzle)
    blank_row_from_bottom = 4 - blank_row
    
    if blank_row_from_bottom % 2 == 1:
        return inversions % 2 == 0
    else:
        return inversions % 2 == 1

def solve_puzzle(puzzle):
    if is_goal(puzzle):
        return ""
    
    if not is_solvable(puzzle):
        return "Unsolvable"
    
    heap = [(manhattan_distance(puzzle), 0, puzzle, "")]
    visited = set()
    visited.add(puzzle_to_tuple(puzzle))
    
    while heap:
        f_score, g_score, current, path = heapq.heappop(heap)
        
        if is_goal(current):
            return path
        
        for neighbor, move in get_neighbors(current):
            neighbor_tuple = puzzle_to_tuple(neighbor)
            if neighbor_tuple not in visited:
                visited.add(neighbor_tuple)
                new_g = g_score + 1
                new_f = new_g + manhattan_distance(neighbor)
                heapq.heappush(heap, (new_f, new_g, neighbor, path + move))
    
    return "Unsolvable"

puzzle = read_input()
result = solve_puzzle(puzzle)
print(result)