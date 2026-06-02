import sys
import csv
from io import StringIO

def main():
    lines = sys.stdin.read().strip().split('\n')
    
    # Parse the first line for mode and parameters
    first_line = lines[0]
    parts = first_line.split()
    mode = parts[0]
    
    # Parse parameters
    params = {}
    for part in parts[1:]:
        key, value = part.split('=')
        params[key] = value
    
    # Read CSV data
    csv_data = '\n'.join(lines[1:])
    reader = csv.DictReader(StringIO(csv_data))
    rows = list(reader)
    
    if mode == 'melt':
        id_col = params['id']
        var_col = params['var']
        val_col = params['val']
        
        # Get all columns except the id column
        all_cols = list(rows[0].keys())
        value_cols = [col for col in all_cols if col != id_col]
        
        # Melt the data
        melted_rows = []
        for row in rows:
            id_value = row[id_col]
            for col in value_cols:
                melted_rows.append({
                    id_col: id_value,
                    var_col: col,
                    val_col: row[col]
                })
        
        # Output
        print(f"{id_col},{var_col},{val_col}")
        for row in melted_rows:
            print(f"{row[id_col]},{row[var_col]},{row[val_col]}")
    
    elif mode == 'pivot':
        id_col = params['id']
        var_col = params['var']
        val_col = params['val']
        
        # Get unique values for pivoting
        pivot_values = sorted(set(row[var_col] for row in rows))
        id_values = sorted(set(row[id_col] for row in rows))
        
        # Create pivot table
        pivot_data = {}
        for row in rows:
            id_val = row[id_col]
            var_val = row[var_col]
            val_val = row[val_col]
            if id_val not in pivot_data:
                pivot_data[id_val] = {}
            pivot_data[id_val][var_val] = val_val
        
        # Output
        header = [id_col] + pivot_values
        print(','.join(header))
        
        for id_val in id_values:
            row_data = [id_val]
            for pivot_val in pivot_values:
                row_data.append(pivot_data[id_val].get(pivot_val, ''))
            print(','.join(row_data))

if __name__ == "__main__":
    main()