import sys
import csv
from io import StringIO

def main():
    # Read all input
    input_data = sys.stdin.read().strip()
    
    # Split by blank line
    parts = input_data.split('\n\n')
    csv_data = parts[0]
    config_line = parts[1]
    
    # Parse configuration
    config_parts = config_line.split()
    rows_col = config_parts[0].split('=')[1]
    pivot_col = config_parts[1].split('=')[1]
    values_col = config_parts[2].split('=')[1]
    agg_func = config_parts[3].split('=')[1]
    
    # Parse CSV data
    csv_reader = csv.DictReader(StringIO(csv_data))
    data = list(csv_reader)
    
    # Get unique values for pivot columns (sorted for consistent output)
    pivot_values = sorted(set(row[pivot_col] for row in data))
    row_values = sorted(set(row[rows_col] for row in data))
    
    # Create pivot table
    pivot_table = {}
    
    for row in data:
        row_key = row[rows_col]
        pivot_key = row[pivot_col]
        value = float(row[values_col])
        
        if row_key not in pivot_table:
            pivot_table[row_key] = {}
        
        if pivot_key not in pivot_table[row_key]:
            pivot_table[row_key][pivot_key] = []
        
        pivot_table[row_key][pivot_key].append(value)
    
    # Aggregate values
    for row_key in pivot_table:
        for pivot_key in pivot_table[row_key]:
            values = pivot_table[row_key][pivot_key]
            if agg_func == 'sum':
                pivot_table[row_key][pivot_key] = sum(values)
            elif agg_func == 'count':
                pivot_table[row_key][pivot_key] = len(values)
            elif agg_func == 'avg':
                pivot_table[row_key][pivot_key] = sum(values) / len(values)
    
    # Output header
    header = [rows_col] + pivot_values
    print(','.join(header))
    
    # Output data rows
    for row_key in row_values:
        row_data = [row_key]
        for pivot_key in pivot_values:
            if row_key in pivot_table and pivot_key in pivot_table[row_key]:
                value = pivot_table[row_key][pivot_key]
                # Format as integer if it's a whole number
                if value == int(value):
                    row_data.append(str(int(value)))
                else:
                    row_data.append(str(value))
            else:
                row_data.append('0')
        print(','.join(row_data))

if __name__ == "__main__":
    main()