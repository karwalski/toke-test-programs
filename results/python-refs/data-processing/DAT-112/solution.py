import sys
import csv
from io import StringIO

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    # Find the blank line that separates operations from CSV
    blank_line_idx = -1
    for i, line in enumerate(lines):
        if line == '':
            blank_line_idx = i
            break
    
    operations = lines[:blank_line_idx]
    csv_lines = lines[blank_line_idx + 1:]
    
    # Parse CSV
    csv_text = '\n'.join(csv_lines)
    csv_reader = csv.DictReader(StringIO(csv_text))
    data = list(csv_reader)
    
    # Process operations
    for op in operations:
        op = op.strip()
        if op.startswith('filter '):
            condition = op[7:]  # Remove 'filter '
            key, value = condition.split('=')
            data = [row for row in data if row[key] == value]
        
        elif op.startswith('group '):
            group_key = op[6:]  # Remove 'group '
            # Store group key for later aggregation
            current_group_key = group_key
        
        elif op.startswith('aggregate '):
            parts = op[10:].split()  # Remove 'aggregate '
            agg_column = parts[0]
            agg_func = parts[1]
            
            # Group data
            groups = {}
            for row in data:
                group_val = row[current_group_key]
                if group_val not in groups:
                    groups[group_val] = []
                groups[group_val].append(row)
            
            # Aggregate
            result = []
            for group_val, group_rows in groups.items():
                if agg_func == 'sum':
                    total = sum(float(row[agg_column]) for row in group_rows)
                    result.append({current_group_key: group_val, f'{agg_column}_{agg_func}': int(total)})
            
            data = result
        
        elif op.startswith('sort '):
            parts = op[5:].split()  # Remove 'sort '
            sort_column = parts[0]
            sort_order = parts[1] if len(parts) > 1 else 'asc'
            
            reverse = (sort_order == 'desc')
            data.sort(key=lambda x: float(x[sort_column]) if str(x[sort_column]).replace('.','').replace('-','').isdigit() else x[sort_column], reverse=reverse)
    
    # Output CSV
    if data:
        fieldnames = list(data[0].keys())
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
        print(output.getvalue().strip())

if __name__ == '__main__':
    main()