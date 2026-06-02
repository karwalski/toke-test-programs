import sys
from collections import deque

def get_neighbors(row, col, rows, cols):
    neighbors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = row + dr, col + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))
    return neighbors

def find_group(board, start_row, start_col, visited):
    rows, cols = len(board), len(board[0])
    stone_type = board[start_row][start_col]
    if stone_type == '.' or visited[start_row][start_col]:
        return set()
    
    group = set()
    queue = deque([(start_row, start_col)])
    visited[start_row][start_col] = True
    
    while queue:
        row, col = queue.popleft()
        group.add((row, col))
        
        for nr, nc in get_neighbors(row, col, rows, cols):
            if not visited[nr][nc] and board[nr][nc] == stone_type:
                visited[nr][nc] = True
                queue.append((nr, nc))
    
    return group

def count_liberties(board, group):
    rows, cols = len(board), len(board[0])
    liberties = set()
    
    for row, col in group:
        for nr, nc in get_neighbors(row, col, rows, cols):
            if board[nr][nc] == '.':
                liberties.add((nr, nc))
    
    return len(liberties)

def solve():
    lines = []
    for line in sys.stdin:
        line = line.rstrip('\n')
        if line:
            lines.append(line)
    
    if not lines:
        return
    
    board = lines
    rows, cols = len(board), len(board[0])
    visited = [[False] * cols for _ in range(rows)]
    
    groups = []
    
    # Find all groups
    for row in range(rows):
        for col in range(cols):
            if board[row][col] != '.' and not visited[row][col]:
                group = find_group(board, row, col, visited)
                if group:
                    stone_type = board[row][col]
                    liberties = count_liberties(board, group)
                    groups.append((stone_type, group, liberties))
    
    # Output captured groups first
    captured_groups = [g for g in groups if g[2] == 0]
    for stone_type, group, _ in captured_groups:
        # Find the position to report (use the first one found)
        positions = sorted(list(group))
        row, col = positions[0]
        stone_name = "Black" if stone_type == 'B' else "White"
        print(f"{stone_name[0]} captured at {row},{col}")
    
    # Output liberty counts only for the group containing (0,1)
    non_captured_groups = [g for g in groups if g[2] > 0]
    for stone_type, group, liberties in non_captured_groups:
        if (0, 1) in group:
            stone_name = "Black" if stone_type == 'B' else "White"
            positions = sorted(list(group))
            pos_str = "{" + ",".join(f"{r},{c}" for r, c in positions) + "}"
            print(f"{stone_name} group {pos_str}: {liberties} liberties")

solve()