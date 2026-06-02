import sys
import csv
import statistics

def read_csv_from_stdin():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    return lines

def parse_csv(lines):
    reader = csv.reader(lines)
    headers = next(reader)
    rows = list(reader)
    return headers, rows

def is_numeric_column(column_data):
    for value in column_data:
        try:
            float(value)
        except ValueError:
            return False
    return True

def compute_quartiles(data):
    sorted_data = sorted(data)
    n = len(sorted_data)
    
    if n == 1:
        return sorted_data[0], sorted_data[0]
    
    # Q1 position (25th percentile)
    q1_pos = (n + 1) * 0.25
    # Q3 position (75th percentile)  
    q3_pos = (n + 1) * 0.75
    
    # Linear interpolation for quartiles
    def get_percentile(pos):
        if pos <= 1:
            return sorted_data[0]
        elif pos >= n:
            return sorted_data[n-1]
        else:
            lower_idx = int(pos) - 1
            upper_idx = lower_idx + 1
            weight = pos - int(pos)
            return sorted_data[lower_idx] + weight * (sorted_data[upper_idx] - sorted_data[lower_idx])
    
    q1 = get_percentile(q1_pos)
    q3 = get_percentile(q3_pos)
    
    return q1, q3

def compute_statistics(data):
    float_data = [float(x) for x in data]
    
    count = len(float_data)
    mean_val = statistics.mean(float_data)
    median_val = statistics.median(float_data)
    stddev_val = statistics.stdev(float_data) if len(float_data) > 1 else 0.0
    min_val = min(float_data)
    max_val = max(float_data)
    q1, q3 = compute_quartiles(float_data)
    
    return {
        'count': count,
        'mean': mean_val,
        'median': median_val,
        'stddev': stddev_val,
        'min': min_val,
        'max': max_val,
        'Q1': q1,
        'Q3': q3
    }

def main():
    lines = read_csv_from_stdin()
    headers, rows = parse_csv(lines)
    
    # Find numeric columns
    numeric_columns = []
    column_data = {}
    
    for i, header in enumerate(headers):
        column_values = [row[i] for row in rows]
        if is_numeric_column(column_values):
            numeric_columns.append(header)
            column_data[header] = column_values
    
    # Compute statistics for each numeric column
    stats_data = {}
    for column in numeric_columns:
        stats_data[column] = compute_statistics(column_data[column])
    
    # Print results
    stat_names = ['count', 'mean', 'median', 'stddev', 'min', 'max', 'Q1', 'Q3']
    
    # Print header
    print("stat", end="")
    for column in numeric_columns:
        print(f"  {column:>6}", end="")
    print()
    
    # Print each statistic row
    for stat in stat_names:
        print(f"{stat:>6}", end="")
        for column in numeric_columns:
            value = stats_data[column][stat]
            if stat == 'count':
                print(f"  {value:>6}", end="")
            else:
                print(f"  {value:>6.2f}", end="")
        print()

if __name__ == "__main__":
    main()