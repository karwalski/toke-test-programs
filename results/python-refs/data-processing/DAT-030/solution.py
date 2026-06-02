import sys
import csv
from io import StringIO

def main():
    # Read all input
    input_text = sys.stdin.read().strip()
    
    # Split by blank line
    parts = input_text.split('\n\n')
    csv_data = parts[0]
    config_line = parts[1]
    
    # Parse CSV data
    csv_reader = csv.DictReader(StringIO(csv_data))
    rows = list(csv_reader)
    
    # Parse configuration
    config_parts = config_line.split(' ')
    group_part = config_parts[0]  # group=dept
    agg_part = config_parts[1]    # agg=salary:avg
    
    # Extract group columns
    group_cols = group_part.split('=')[1].split(',')
    
    # Extract aggregation specifications
    agg_specs = config_parts[1:]  # All parts starting with agg=
    agg_funcs = []
    
    for spec in agg_specs:
        if spec.startswith('agg='):
            agg_data = spec[4:]  # Remove 'agg='
            # Split by spaces to handle multiple column:function pairs
            pairs = agg_data.split(' ')
            for pair in pairs:
                if ':' in pair:
                    col, func = pair.split(':')
                    agg_funcs.append((col, func))
        else:
            # This is an additional column:function pair
            if ':' in spec:
                col, func = spec.split(':')
                agg_funcs.append((col, func))
    
    # Group data
    groups = {}
    for row in rows:
        # Create group key
        group_key = tuple(row[col] for col in group_cols)
        
        if group_key not in groups:
            groups[group_key] = []
        groups[group_key].append(row)
    
    # Compute aggregates
    result_rows = []
    for group_key, group_rows in groups.items():
        result_row = {}
        
        # Add group columns
        for i, col in enumerate(group_cols):
            result_row[col] = group_key[i]
        
        # Add aggregated columns
        for col, func in agg_funcs:
            values = [float(row[col]) for row in group_rows]
            
            if func == 'sum':
                result = sum(values)
                result_row[f"{col}_{func}"] = f"{result:.2f}"
            elif func == 'count':
                result = len(values)
                result_row[f"{col}_{func}"] = str(result)
            elif func == 'avg':
                result = sum(values) / len(values)
                result_row[f"{col}_{func}"] = f"{result:.2f}"
            elif func == 'min':
                result = min(values)
                result_row[f"{col}_{func}"] = f"{result:.2f}"
            elif func == 'max':
                result = max(values)
                result_row[f"{col}_{func}"] = f"{result:.2f}"
        
        result_rows.append(result_row)
    
    # Sort by group keys for consistent output
    result_rows.sort(key=lambda x: tuple(x[col] for col in group_cols))
    
    # Output CSV
    if result_rows:
        # Build header
        header = group_cols + [f"{col}_{func}" for col, func in agg_funcs]
        
        # Write output
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=header, lineterminator='\n')
        writer.writeheader()
        writer.writerows(result_rows)
        
        print(output.getvalue().strip())

if __name__ == "__main__":
    main()