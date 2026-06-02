import sys
import csv
from io import StringIO

def parse_input():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    # Find the separator between datasets and join condition
    dataset1_lines = []
    dataset2_lines = []
    join_line = ""
    
    current_dataset = 1
    blank_count = 0
    
    for line in lines:
        if line == "":
            blank_count += 1
            if blank_count == 1:
                current_dataset = 2
            continue
        
        if line.startswith("join "):
            join_line = line
            break
        
        if current_dataset == 1:
            dataset1_lines.append(line)
        else:
            dataset2_lines.append(line)
    
    return dataset1_lines, dataset2_lines, join_line

def parse_csv_lines(lines):
    if not lines:
        return [], []
    
    reader = csv.reader(lines)
    rows = list(reader)
    headers = rows[0] if rows else []
    data = rows[1:] if len(rows) > 1 else []
    
    return headers, data

def hash_join():
    dataset1_lines, dataset2_lines, join_line = parse_input()
    
    # Parse join condition
    join_part = join_line.replace("join ", "")
    left_col, right_col = join_part.split("=")
    
    # Parse datasets
    build_headers, build_data = parse_csv_lines(dataset1_lines)
    probe_headers, probe_data = parse_csv_lines(dataset2_lines)
    
    build_size = len(build_data)
    probe_size = len(probe_data)
    
    # Find column indices
    left_col_idx = build_headers.index(left_col)
    right_col_idx = probe_headers.index(right_col)
    
    # Build phase: create hash table
    hash_table = {}
    for row in build_data:
        key = row[left_col_idx]
        if key not in hash_table:
            hash_table[key] = []
        hash_table[key].append(row)
    
    # Probe phase: find matches
    matches = []
    match_count = 0
    
    for probe_row in probe_data:
        probe_key = probe_row[right_col_idx]
        if probe_key in hash_table:
            for build_row in hash_table[probe_key]:
                match_count += 1
                # Combine rows
                combined_row = build_row + [col for i, col in enumerate(probe_row) if i != right_col_idx]
                matches.append(combined_row)
    
    # Create output headers
    output_headers = build_headers + [col for i, col in enumerate(probe_headers) if i != right_col_idx]
    
    # Print statistics
    print(f"Build table: {build_size} rows")
    print(f"Probe table: {probe_size} rows")
    print(f"Matches: {match_count}")
    
    # Print joined CSV
    print(",".join(output_headers))
    for match in matches:
        print(",".join(match))

if __name__ == "__main__":
    hash_join()