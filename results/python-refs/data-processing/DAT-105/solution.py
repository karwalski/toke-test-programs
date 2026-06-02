import sys
import re

def extract_tables_from_markdown(text):
    lines = text.strip().split('\n')
    tables = []
    current_table = []
    in_table = False
    
    for line in lines:
        # Check if line looks like a table row (contains |)
        if '|' in line.strip():
            # Remove leading/trailing whitespace and outer pipes
            cleaned_line = line.strip()
            if cleaned_line.startswith('|'):
                cleaned_line = cleaned_line[1:]
            if cleaned_line.endswith('|'):
                cleaned_line = cleaned_line[:-1]
            
            # Split by | and clean each cell
            cells = [cell.strip() for cell in cleaned_line.split('|')]
            
            # Check if this is a separator row (contains only -, :, |, and whitespace)
            if re.match(r'^[\s\-:|]*$', cleaned_line):
                # This is a separator row, skip it
                continue
            
            if not in_table:
                in_table = True
                current_table = []
            
            current_table.append(cells)
        else:
            # Not a table row
            if in_table:
                # End of current table
                if current_table:
                    tables.append(current_table)
                current_table = []
                in_table = False
    
    # Don't forget the last table if the text ends with a table
    if in_table and current_table:
        tables.append(current_table)
    
    return tables

def table_to_csv(table):
    csv_lines = []
    for row in table:
        csv_lines.append(','.join(row))
    return '\n'.join(csv_lines)

# Read input from stdin
input_text = sys.stdin.read()

# Extract tables
tables = extract_tables_from_markdown(input_text)

# Convert each table to CSV and output
for i, table in enumerate(tables):
    if i > 0:
        print()  # Blank line between tables
    print(table_to_csv(table))