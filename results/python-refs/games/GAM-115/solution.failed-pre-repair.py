import sys
from collections import defaultdict

def get_neighbors(r, c):
    return [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]

def normalize_shape(coords):
    """Normalize a shape by translating to origin and sorting"""
    if not coords:
        return []
    
    min_r = min(r for r, c in coords)
    min_c = min(c for r, c in coords)
    
    normalized = [(r - min_r, c - min_c) for r, c in coords]
    return sorted(normalized)

def get_rotations_and_reflections(coords):
    """Get all possible rotations and reflections of a shape"""
    shapes = set()
    
    # Original
    shapes.add(tuple(normalize_shape(coords)))
    
    # Rotate 90, 180, 270 degrees
    for _ in range(3):
        coords = [(-c, r) for r, c in coords]
        shapes.add(tuple(normalize_shape(coords)))
    
    # Reflect and repeat rotations
    coords = [(r, -c) for r, c in coords]
    shapes.add(tuple(normalize_shape(coords)))
    
    for _ in range(3):
        coords = [(-c, r) for r, c in coords]
        shapes.add(tuple(normalize_shape(coords)))
    
    return shapes

def is_valid_tetromino(coords):
    """Check if coordinates form a valid tetromino"""
    if len(coords) != 4:
        return False
    
    # Check if all squares are connected
    coords_set = set(coords)
    visited = set()
    stack = [coords[0]]
    
    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        
        for neighbor in get_neighbors(current[0], current[1]):
            if neighbor in coords_set and neighbor not in visited:
                stack.append(neighbor)
    
    if len(visited) != 4:
        return False
    
    # Define all valid tetromino shapes (normalized)
    valid_tetrominoes = set()
    
    # I-piece
    i_piece = [(0, 0), (0, 1), (0, 2), (0, 3)]
    valid_tetrominoes.update(get_rotations_and_reflections(i_piece))
    
    # O-piece
    o_piece = [(0, 0), (0, 1), (1, 0), (1, 1)]
    valid_tetrominoes.update(get_rotations_and_reflections(o_piece))
    
    # T-piece
    t_piece = [(0, 1), (1, 0), (1, 1), (1, 2)]
    valid_tetrominoes.update(get_rotations_and_reflections(t_piece))
    
    # S-piece
    s_piece = [(0, 1), (0, 2), (1, 0), (1, 1)]
    valid_tetrominoes.update(get_rotations_and_reflections(s_piece))
    
    # Z-piece
    z_piece = [(0, 0), (0, 1), (1, 1), (1, 2)]
    valid_tetrominoes.update(get_rotations_and_reflections(z_piece))
    
    # J-piece
    j_piece = [(0, 0), (1, 0), (1, 1), (1, 2)]
    valid_tetrominoes.update(get_rotations_and_reflections(j_piece))
    
    # L-piece
    l_piece = [(0, 2), (1, 0), (1, 1), (1, 2)]
    valid_tetrominoes.update(get_rotations_and_reflections(l_piece))
    
    # Check if our shape matches any valid tetromino
    our_shape = tuple(normalize_shape(coords))
    return our_shape in valid_tetrominoes

def main():
    lines = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            lines.append(line)
    
    if not lines:
        return
    
    # Parse grid
    grid = []
    for line in lines:
        row = [int(c) for c in line if c.isdigit()]
        grid.append(row)
    
    # Group coordinates by piece ID
    pieces = defaultdict(list)
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] != 0:
                pieces[grid[r][c]].append((r, c))
    
    # Check each piece
    for piece_id in sorted(pieces.keys()):
        coords = pieces[piece_id]
        if not is_valid_tetromino(coords):
            print(f"Invalid: piece {piece_id} is not a valid tetromino")
            return
    
    print("Valid tiling")

if __name__ == "__main__":
    main()