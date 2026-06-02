import sys

def solve_lights_out():
    # Read input
    lines = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            lines.append(line)
    
    if not lines:
        return
    
    rows = len(lines)
    cols = len(lines[0])
    
    # Parse initial state
    grid = []
    for line in lines:
        grid.append([int(c) for c in line])
    
    # Create the coefficient matrix
    # Each row represents one light's equation
    # Each column represents one button
    n = rows * cols
    matrix = []
    target = []
    
    for r in range(rows):
        for c in range(cols):
            # Equation for light at (r, c)
            equation = [0] * n
            
            # Check which buttons affect this light
            for br in range(rows):
                for bc in range(cols):
                    button_idx = br * cols + bc
                    
                    # Button affects this light if it's the same position
                    # or orthogonally adjacent
                    if (br == r and bc == c) or \
                       (br == r and abs(bc - c) == 1) or \
                       (bc == c and abs(br - r) == 1):
                        equation[button_idx] = 1
            
            matrix.append(equation)
            target.append(grid[r][c])  # We want to turn ON lights that are currently OFF
    
    # Solve using Gaussian elimination over GF(2)
    solution = gaussian_elimination_gf2(matrix, target)
    
    if solution is None:
        print("Unsolvable")
    else:
        # Output button positions
        presses = []
        for i, press in enumerate(solution):
            if press == 1:
                r = i // cols
                c = i % cols
                presses.append((r, c))
        
        for r, c in presses:
            print(f"{r} {c}")

def gaussian_elimination_gf2(matrix, target):
    """Solve Ax = b over GF(2) using Gaussian elimination"""
    n = len(matrix)
    m = len(matrix[0])
    
    # Augment matrix with target
    aug = []
    for i in range(n):
        aug.append(matrix[i][:] + [target[i]])
    
    # Forward elimination
    pivot_row = 0
    for col in range(m):
        # Find pivot
        pivot_found = False
        for row in range(pivot_row, n):
            if aug[row][col] == 1:
                # Swap rows
                aug[pivot_row], aug[row] = aug[row], aug[pivot_row]
                pivot_found = True
                break
        
        if not pivot_found:
            continue
        
        # Eliminate column
        for row in range(n):
            if row != pivot_row and aug[row][col] == 1:
                for j in range(m + 1):
                    aug[row][j] ^= aug[pivot_row][j]
        
        pivot_row += 1
    
    # Check for inconsistency
    for row in range(pivot_row, n):
        if aug[row][m] == 1:
            return None  # Inconsistent system
    
    # Back substitution to find particular solution
    solution = [0] * m
    
    for row in range(min(pivot_row, m) - 1, -1, -1):
        # Find the pivot column for this row
        pivot_col = -1
        for col in range(m):
            if aug[row][col] == 1:
                pivot_col = col
                break
        
        if pivot_col != -1:
            # Calculate value for this variable
            val = aug[row][m]
            for col in range(pivot_col + 1, m):
                val ^= aug[row][col] * solution[col]
            solution[pivot_col] = val
    
    return solution

if __name__ == "__main__":
    solve_lights_out()