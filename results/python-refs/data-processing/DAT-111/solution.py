import sys
import csv
from io import StringIO

def parse_query(query):
    query = query.strip()
    parts = {}
    
    # Split by keywords
    keywords = ['SELECT', 'FROM', 'WHERE', 'ORDER BY', 'GROUP BY', 'LIMIT']
    current_keyword = None
    current_text = ""
    
    tokens = query.split()
    i = 0
    while i < len(tokens):
        token = tokens[i].upper()
        if token in keywords:
            if current_keyword:
                parts[current_keyword] = current_text.strip()
            current_keyword = token
            current_text = ""
        elif token == 'BY' and i > 0 and tokens[i-1].upper() in ['ORDER', 'GROUP']:
            # Handle ORDER BY and GROUP BY
            current_keyword = tokens[i-1].upper() + ' BY'
            current_text = ""
        else:
            if current_keyword:
                current_text += " " + tokens[i]
        i += 1
    
    if current_keyword:
        parts[current_keyword] = current_text.strip()
    
    return parts

def evaluate_condition(row, condition, headers):
    # Simple condition parsing for WHERE clause
    condition = condition.strip()
    
    # Handle basic comparisons
    operators = ['>=', '<=', '!=', '>', '<', '=']
    for op in operators:
        if op in condition:
            left, right = condition.split(op, 1)
            left = left.strip()
            right = right.strip()
            
            # Remove quotes if present
            if right.startswith("'") and right.endswith("'"):
                right = right[1:-1]
            
            if left in headers:
                col_idx = headers.index(left)
                left_val = row[col_idx]
                
                # Try to convert to number if possible
                try:
                    left_val = float(left_val)
                    right = float(right)
                except ValueError:
                    pass
                
                if op == '>':
                    return left_val > right
                elif op == '<':
                    return left_val < right
                elif op == '>=':
                    return left_val >= right
                elif op == '<=':
                    return left_val <= right
                elif op == '=' or op == '==':
                    return left_val == right
                elif op == '!=':
                    return left_val != right
    
    return True

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    if len(lines) < 2:
        return
    
    query = lines[0]
    csv_data = '\n'.join(lines[1:])
    
    # Parse CSV
    csv_reader = csv.reader(StringIO(csv_data))
    rows = list(csv_reader)
    
    if not rows:
        return
    
    headers = rows[0]
    data_rows = rows[1:]
    
    # Parse query
    parts = parse_query(query)
    
    # Get selected columns
    select_cols = [col.strip() for col in parts.get('SELECT', '').split(',')]
    
    # Filter rows based on WHERE clause
    filtered_rows = data_rows
    if 'WHERE' in parts:
        condition = parts['WHERE']
        filtered_rows = [row for row in filtered_rows if evaluate_condition(row, condition, headers)]
    
    # Select only required columns
    if select_cols and select_cols != ['']:
        col_indices = []
        for col in select_cols:
            if col in headers:
                col_indices.append(headers.index(col))
        
        result_headers = select_cols
        result_rows = []
        for row in filtered_rows:
            result_row = [row[i] for i in col_indices]
            result_rows.append(result_row)
    else:
        result_headers = headers
        result_rows = filtered_rows
    
    # Order by
    if 'ORDER BY' in parts:
        order_clause = parts['ORDER BY'].strip()
        desc = False
        if order_clause.upper().endswith(' DESC'):
            desc = True
            order_clause = order_clause[:-5].strip()
        elif order_clause.upper().endswith(' ASC'):
            order_clause = order_clause[:-4].strip()
        
        if order_clause in result_headers:
            col_idx = result_headers.index(order_clause)
            def sort_key(row):
                val = row[col_idx]
                try:
                    return float(val)
                except ValueError:
                    return val
            
            result_rows.sort(key=sort_key, reverse=desc)
    
    # Limit
    if 'LIMIT' in parts:
        try:
            limit = int(parts['LIMIT'].strip())
            result_rows = result_rows[:limit]
        except ValueError:
            pass
    
    # Output results
    print(','.join(result_headers))
    for row in result_rows:
        print(','.join(str(cell) for cell in row))

if __name__ == "__main__":
    main()