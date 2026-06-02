import sys

def edges_match(edge1, edge2):
    """Check if two edges can connect"""
    if edge1 == '0' and edge2 == '0':
        return True
    if edge1 == '+' and edge2 == '-':
        return True
    if edge1 == '-' and edge2 == '+':
        return True
    return False

def main():
    pieces = {}
    
    # Read input
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) == 5:
            piece_id = parts[0]
            top, right, bottom, left = parts[1], parts[2], parts[3], parts[4]
            pieces[piece_id] = {
                'top': top,
                'right': right,
                'bottom': bottom,
                'left': left
            }
    
    adjacent_pairs = []
    
    # Check all pairs of pieces
    for piece1_id, piece1 in pieces.items():
        for piece2_id, piece2 in pieces.items():
            if piece1_id == piece2_id:
                continue
            
            # Check if piece1 can be right of piece2
            if edges_match(piece2['right'], piece1['left']):
                adjacent_pairs.append(f"{piece1_id} right of {piece2_id}")
            
            # Check if piece1 can be below piece2
            if edges_match(piece2['bottom'], piece1['top']):
                adjacent_pairs.append(f"{piece1_id} below {piece2_id}")
    
    # Sort and output
    adjacent_pairs.sort()
    for pair in adjacent_pairs:
        print(pair)

if __name__ == "__main__":
    main()