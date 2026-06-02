import sys
import csv
import random
from io import StringIO

def read_input():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    return lines

def parse_strategy_line(line):
    parts = line.split()
    strategy = parts[0]
    
    if strategy == 'systematic':
        return strategy, {'k': int(parts[1])}, None
    elif strategy == 'stratified':
        return strategy, {'n': int(parts[1]), 'column': parts[2]}, int(parts[3]) if len(parts) > 3 else None
    elif strategy == 'reservoir':
        return strategy, {'k': int(parts[1])}, int(parts[2]) if len(parts) > 2 else None
    
    return strategy, {}, None

def systematic_sampling(data, k):
    if k <= 0 or len(data) == 0:
        return []
    
    # Sample every k-th element starting from index 0
    result = []
    for i in range(0, len(data), k):
        result.append(data[i])
    
    return result

def stratified_sampling(data, n, column, seed):
    if seed is not None:
        random.seed(seed)
    
    # Group data by the stratification column
    strata = {}
    header = data[0]
    col_index = header.index(column)
    
    for row in data[1:]:
        stratum_value = row[col_index]
        if stratum_value not in strata:
            strata[stratum_value] = []
        strata[stratum_value].append(row)
    
    # Sample n items from each stratum
    result = [header]
    for stratum_value, stratum_data in strata.items():
        sample_size = min(n, len(stratum_data))
        sampled = random.sample(stratum_data, sample_size)
        result.extend(sampled)
    
    return result

def reservoir_sampling(data, k, seed):
    if seed is not None:
        random.seed(seed)
    
    if len(data) <= 1:
        return data
    
    header = data[0]
    rows = data[1:]
    
    if k >= len(rows):
        return data
    
    # Reservoir sampling algorithm
    reservoir = rows[:k]
    
    for i in range(k, len(rows)):
        j = random.randint(0, i)
        if j < k:
            reservoir[j] = rows[i]
    
    return [header] + reservoir

def main():
    lines = read_input()
    
    strategy, params, seed = parse_strategy_line(lines[0])
    
    # Parse CSV data
    csv_lines = lines[1:]
    csv_input = StringIO('\n'.join(csv_lines))
    reader = csv.reader(csv_input)
    data = list(reader)
    
    if strategy == 'systematic':
        result = systematic_sampling(data, params['k'])
    elif strategy == 'stratified':
        result = stratified_sampling(data, params['n'], params['column'], seed)
    elif strategy == 'reservoir':
        result = reservoir_sampling(data, params['k'], seed)
    else:
        result = data
    
    # Output CSV
    output = StringIO()
    writer = csv.writer(output)
    for row in result:
        writer.writerow(row)
    
    print(output.getvalue().rstrip())

if __name__ == '__main__':
    main()