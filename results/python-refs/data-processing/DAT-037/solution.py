import sys
import json
import csv
from io import StringIO

def read_input():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    # Find the blank line that separates JSON from CSV
    blank_line_idx = -1
    for i, line in enumerate(lines):
        if line == '':
            blank_line_idx = i
            break
    
    json_lines = lines[:blank_line_idx]
    csv_lines = lines[blank_line_idx + 1:]
    
    pipeline_def = json.loads(''.join(json_lines))
    csv_data = '\n'.join(csv_lines)
    
    return pipeline_def, csv_data

def parse_csv(csv_data):
    reader = csv.DictReader(StringIO(csv_data))
    rows = list(reader)
    return rows

def filter_rows(rows, expr):
    filtered = []
    for row in rows:
        # Convert numeric values for evaluation
        eval_context = {}
        for key, value in row.items():
            try:
                eval_context[key] = int(value)
            except ValueError:
                try:
                    eval_context[key] = float(value)
                except ValueError:
                    eval_context[key] = value
        
        if eval(expr, {"__builtins__": {}}, eval_context):
            filtered.append(row)
    
    return filtered

def select_columns(rows, cols):
    selected = []
    for row in rows:
        new_row = {col: row[col] for col in cols if col in row}
        selected.append(new_row)
    return selected

def sort_rows(rows, by):
    return sorted(rows, key=lambda x: x[by])

def execute_pipeline(pipeline_def, csv_data):
    rows = parse_csv(csv_data)
    
    for step in pipeline_def['steps']:
        op = step['op']
        
        if op == 'filter':
            rows = filter_rows(rows, step['expr'])
        elif op == 'select':
            rows = select_columns(rows, step['cols'])
        elif op == 'sort':
            rows = sort_rows(rows, step['by'])
    
    return rows

def write_csv(rows):
    if not rows:
        return
    
    output = StringIO()
    fieldnames = list(rows[0].keys())
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    
    writer.writeheader()
    writer.writerows(rows)
    
    result = output.getvalue().rstrip('\n')
    print(result)

def main():
    pipeline_def, csv_data = read_input()
    result_rows = execute_pipeline(pipeline_def, csv_data)
    write_csv(result_rows)

if __name__ == "__main__":
    main()