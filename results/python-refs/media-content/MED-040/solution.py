import sys

def align_markdown_table():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    if not lines:
        return
    
    # Parse all rows into columns
    rows = []
    for line in lines:
        # Split by | and strip whitespace, remove empty first/last elements
        cols = [col.strip() for col in line.split('|')]
        if cols[0] == '':
            cols = cols[1:]
        if cols and cols[-1] == '':
            cols = cols[:-1]
        rows.append(cols)
    
    if not rows:
        return
    
    # Find maximum width for each column
    num_cols = len(rows[0])
    col_widths = [0] * num_cols
    
    for row in rows:
        for i, col in enumerate(row):
            col_widths[i] = max(col_widths[i], len(col))
    
    # Output aligned table
    for row in rows:
        padded_cols = []
        for i, col in enumerate(row):
            if col.startswith('-') and all(c == '-' for c in col):
                # This is a separator row, pad with dashes
                padded_cols.append('-' * col_widths[i])
            else:
                # Regular content, left-align with spaces
                padded_cols.append(col.ljust(col_widths[i]))
        
        print('| ' + ' | '.join(padded_cols) + ' |')

align_markdown_table()