def generate_arrangements(clues, length):
    """Generate all possible arrangements for given clues in a row of given length."""
    if not clues:
        return [['O'] * length]
    
    arrangements = []
    
    def backtrack(pos, clue_idx, current):
        if clue_idx == len(clues):
            # All clues placed, fill remaining with empty
            result = current + ['O'] * (length - len(current))
            if len(result) == length:
                arrangements.append(result)
            return
        
        if pos >= length:
            return
        
        clue_size = clues[clue_idx]
        min_space_needed = sum(clues[clue_idx+1:]) + len(clues) - clue_idx - 1
        
        # Try placing the current clue at different positions
        max_start = length - clue_size - min_space_needed
        
        for start in range(pos, max_start + 1):
            # Add empty cells before the clue
            new_current = current + ['O'] * (start - pos) + ['X'] * clue_size
            
            # Add separator if not the last clue
            if clue_idx < len(clues) - 1:
                new_current.append('O')
                backtrack(len(new_current), clue_idx + 1, new_current)
            else:
                backtrack(len(new_current), clue_idx + 1, new_current)
    
    backtrack(0, 0, [])
    return arrangements

def is_compatible(arrangement, current_state):
    """Check if an arrangement is compatible with the current state."""
    for i, (arr_cell, curr_cell) in enumerate(zip(arrangement, current_state)):
        if curr_cell != '.' and arr_cell != curr_cell:
            return False
    return True

def solve_nonogram_row(length, clues, current_state):
    """Solve a single nonogram row."""
    # Generate all possible arrangements
    all_arrangements = generate_arrangements(clues, length)
    
    # Filter arrangements that are compatible with current state
    compatible_arrangements = []
    for arr in all_arrangements:
        if is_compatible(arr, current_state):
            compatible_arrangements.append(arr)
    
    # Find definite cells
    result = ['.'] * length
    for i in range(length):
        if compatible_arrangements:
            first_cell = compatible_arrangements[0][i]
            if all(arr[i] == first_cell for arr in compatible_arrangements):
                result[i] = first_cell
    
    return ''.join(result)

# Read input
length = int(input())
clues_line = input().strip()
if clues_line:
    clues = list(map(int, clues_line.split()))
else:
    clues = []
current_state = input().strip()

# Solve and output
result = solve_nonogram_row(length, clues, current_state)
print(result)