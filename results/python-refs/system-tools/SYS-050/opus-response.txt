import sys

data = sys.stdin.read()
lines = data.split('\n')

# Parse first 3 lines - they may contain tabs
# Test 1: '|\t|\tleft' - separator_in='|', then tab, separator_out='|', then tab, alignment='left'
# So first line contains all three config items separated by tabs? No wait.
# Looking again: 'Line 1: separator_in. Line 2: separator_out. Line 3: alignment'
# But test 1 input is '|\t|\tleft\nfoo|bar|baz\na|bb|ccc'
# Split by \n: ['|\t|\tleft', 'foo|bar|baz', 'a|bb|ccc']
# So line 1 has separator_in, separator_out, alignment all tab-separated

first = lines[0].split('\t')
separator_in = first[0]
separator_out = first[1]
alignment = first[2]
data_lines = lines[1:]

rows = []
max_cols = 0
for line in data_lines:
    cols = line.split(separator_in)
    rows.append(cols)
    max_cols = max(max_cols, len(cols))

col_widths = [0] * max_cols
for row in rows:
    for i, col in enumerate(row):
        col_widths[i] = max(col_widths[i], len(col))

out_lines = []
for row in rows:
    formatted_cols = []
    for i in range(max_cols):
        text = row[i] if i < len(row) else ""
        width = col_widths[i]
        if alignment == "left":
            formatted = text.ljust(width)
        elif alignment == "right":
            formatted = text.rjust(width)
        else:
            formatted = text.center(width)
        formatted_cols.append(formatted)
    out_lines.append(separator_out.join(formatted_cols))

print('\n'.join(out_lines))