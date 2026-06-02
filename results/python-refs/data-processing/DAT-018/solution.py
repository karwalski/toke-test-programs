import sys
from itertools import combinations

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

def find_groups(rows, column_name, threshold):
    column_index = None
    headers = rows[0]
    for i, header in enumerate(headers):
        if header == column_name:
            column_index = i
            break
    
    if column_index is None:
        return []
    
    # Create groups using union-find approach
    groups = []
    used = set()
    
    for i in range(1, len(rows)):
        if i in used:
            continue
            
        current_group = [i]
        used.add(i)
        
        # Find all rows similar to current row
        for j in range(i + 1, len(rows)):
            if j in used:
                continue
                
            distance = levenshtein_distance(rows[i][column_index], rows[j][column_index])
            if distance <= threshold:
                current_group.append(j)
                used.add(j)
        
        # Check if any rows in current group are similar to remaining rows
        changed = True
        while changed:
            changed = False
            for group_idx in current_group[:]:
                for j in range(1, len(rows)):
                    if j in used:
                        continue
                    distance = levenshtein_distance(rows[group_idx][column_index], rows[j][column_index])
                    if distance <= threshold:
                        current_group.append(j)
                        used.add(j)
                        changed = True
        
        groups.append(current_group)
    
    return groups

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

# Find the blank line separator
blank_line_index = -1
for i, line in enumerate(lines):
    if line == '':
        blank_line_index = i
        break

# Parse CSV data
csv_lines = lines[:blank_line_index]
rows = []
for line in csv_lines:
    rows.append(line.split(','))

# Parse parameters
params_line = lines[blank_line_index + 1]
parts = params_line.split(' ')
column_name = parts[0].split('=')[1]
threshold = int(parts[1].split('=')[1])

# Find groups
groups = find_groups(rows, column_name, threshold)

# Output groups
for i, group in enumerate(groups):
    if i > 0:
        print()
    
    for row_index in group:
        print(','.join(rows[row_index]))