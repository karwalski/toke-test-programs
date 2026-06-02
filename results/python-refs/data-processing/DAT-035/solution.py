import sys
import csv
from io import StringIO

def parse_input():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    # Find blank lines to split sections
    blank_indices = []
    for i, line in enumerate(lines):
        if line == '':
            blank_indices.append(i)
    
    # Extract dataset A (old)
    dataset_a_lines = lines[:blank_indices[0]]
    
    # Extract dataset B (new)
    dataset_b_lines = lines[blank_indices[0]+1:blank_indices[1]]
    
    # Extract key column
    key_column = lines[blank_indices[1]+1]
    
    return dataset_a_lines, dataset_b_lines, key_column

def parse_csv_data(lines):
    if not lines:
        return [], {}
    
    csv_text = '\n'.join(lines)
    reader = csv.reader(StringIO(csv_text))
    rows = list(reader)
    
    if not rows:
        return [], {}
    
    headers = rows[0]
    data_rows = rows[1:]
    
    return headers, data_rows

def compare_datasets():
    dataset_a_lines, dataset_b_lines, key_column = parse_input()
    
    headers_a, rows_a = parse_csv_data(dataset_a_lines)
    headers_b, rows_b = parse_csv_data(dataset_b_lines)
    
    # Find key column index
    key_index = headers_a.index(key_column)
    
    # Create dictionaries keyed by the key column value
    dict_a = {}
    for row in rows_a:
        key_val = row[key_index]
        dict_a[key_val] = row
    
    dict_b = {}
    for row in rows_b:
        key_val = row[key_index]
        dict_b[key_val] = row
    
    # Find changes
    changes = []
    
    # Check for removed rows (in A but not in B)
    for key in dict_a:
        if key not in dict_b:
            row_str = ','.join(dict_a[key])
            changes.append(('removed', key, f"- {row_str}"))
    
    # Check for changed rows (in both A and B but different)
    for key in dict_a:
        if key in dict_b:
            if dict_a[key] != dict_b[key]:
                # Find what changed
                old_row = dict_a[key]
                new_row = dict_b[key]
                
                # Find the first differing column that's not the key
                for i, (old_val, new_val) in enumerate(zip(old_row, new_row)):
                    if old_val != new_val and i != key_index:
                        changes.append(('changed', key, f"~ {key}: {old_val} -> {new_val}"))
                        break
    
    # Check for added rows (in B but not in A)
    for key in dict_b:
        if key not in dict_a:
            row_str = ','.join(dict_b[key])
            changes.append(('added', key, f"+ {row_str}"))
    
    # Sort changes by key for consistent output
    changes.sort(key=lambda x: x[1])
    
    # Output in the order: removed, changed, added
    for change_type in ['removed', 'changed', 'added']:
        for change in changes:
            if change[0] == change_type:
                print(change[2])

compare_datasets()