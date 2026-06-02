import sys
from collections import defaultdict

def get_neighbors(r, c):
    return [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]

def normalize_shape(coords):
    if not coords:
        return []
    min_r = min(r for r, c in coords)
    min_c = min(c for r, c in coords)
    return sorted([(r - min_r, c - min_c) for r, c in coords])

def get_rotations_and_reflections(coords):
    shapes = set()
    shapes.add(tuple(normalize_shape(coords)))
    cur = list(coords)
    for _ in range(3):
        cur = [(-c, r) for r, c in cur]
        shapes.add(tuple(normalize_shape(cur)))
    cur = [(r, -c) for r, c in coords]
    shapes.add(tuple(normalize_shape(cur)))
    for _ in range(3):
        cur = [(-c, r) for r, c in cur]
        shapes.add(tuple(normalize_shape(cur)))
    return shapes

VALID = set()
for piece in [
    [(0,0),(0,1),(0,2),(0,3)],
    [(0,0),(0,1),(1,0),(1,1)],
    [(0,1),(1,0),(1,1),(1,2)],
    [(0,1),(0,2),(1,0),(1,1)],
    [(0,0),(0,1),(1,1),(1,2)],
    [(0,0),(1,0),(1,1),(1,2)],
    [(0,2),(1,0),(1,1),(1,2)],
]:
    VALID.update(get_rotations_and_reflections(piece))

def is_connected_tetromino(coords):
    if len(coords) != 4:
        return False
    coords_set = set(coords)
    visited = set()
    stack = [coords[0]]
    while stack:
        cur = stack.pop()
        if cur in visited:
            continue
        visited.add(cur)
        for n in get_neighbors(*cur):
            if n in coords_set and n not in visited:
                stack.append(n)
    if len(visited) != 4:
        return False
    return tuple(normalize_shape(coords)) in VALID

def main():
    lines = [l.strip() for l in sys.stdin if l.strip()]
    if not lines:
        return
    grid = [[int(c) for c in line if c.isdigit()] for line in lines]
    pieces = defaultdict(list)
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] != 0:
                pieces[grid[r][c]].append((r, c))
    # Find first invalid by scanning grid order
    seen = set()
    order = []
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            pid = grid[r][c]
            if pid != 0 and pid not in seen:
                seen.add(pid)
                order.append(pid)
    for pid in order:
        if not is_connected_tetromino(pieces[pid]):
            print(f"Invalid: piece {pid} is not a valid tetromino")
            return
    print("Valid tiling")

main()