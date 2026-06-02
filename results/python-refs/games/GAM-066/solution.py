import sys

def parse_input():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    # Find the grid
    grid_lines = []
    i = 0
    while i < len(lines) and lines[i] != '':
        grid_lines.append(lines[i])
        i += 1
    
    # Skip blank line
    i += 1
    
    # Read row clues
    row_clues = []
    while i < len(lines) and lines[i] != '':
        row_clues.append(int(lines[i]))
        i += 1
    
    # Skip blank line
    i += 1
    
    # Read column clues
    col_clues = []
    while i < len(lines):
        col_clues.append(int(lines[i]))
        i += 1
    
    return grid_lines, row_clues, col_clues

def get_run_lengths(sequence):
    runs = []
    current_run = 0
    
    for cell in sequence:
        if cell == 'X':
            current_run += 1
        else:
            if current_run > 0:
                runs.append(current_run)
                current_run = 0
    
    if current_run > 0:
        runs.append(current_run)
    
    return runs

def validate_picross():
    grid_lines, row_clues, col_clues = parse_input()
    
    # Check rows
    for i, row in enumerate(grid_lines):
        runs = get_run_lengths(row)
        if len(runs) == 0:
            expected_runs = [0] if row_clues[i] == 0 else []
        else:
            expected_runs = runs
        
        if len(expected_runs) != 1 or (len(expected_runs) == 1 and expected_runs[0] != row_clues[i]):
            if row_clues[i] == 0 and len(runs) == 0:
                continue
            elif row_clues[i] != 0 and len(runs) == 1 and runs[0] == row_clues[i]:
                continue
            else:
                print(f"Invalid: row {i + 1}")
                return
    
    # Check columns
    for j in range(len(grid_lines[0])):
        col = ''.join(grid_lines[i][j] for i in range(len(grid_lines)))
        runs = get_run_lengths(col)
        
        if len(runs) == 0:
            expected_runs = [0] if col_clues[j] == 0 else []
        else:
            expected_runs = runs
        
        if len(expected_runs) != 1 or (len(expected_runs) == 1 and expected_runs[0] != col_clues[j]):
            if col_clues[j] == 0 and len(runs) == 0:
                continue
            elif col_clues[j] != 0 and len(runs) == 1 and runs[0] == col_clues[j]:
                continue
            else:
                print(f"Invalid: col {j + 1}")
                return
    
    print("Valid")

validate_picross()