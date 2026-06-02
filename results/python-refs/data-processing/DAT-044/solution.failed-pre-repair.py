import sys

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

# Parse code table
code_table = {}
i = 0
while i < len(lines) and lines[i].strip() != '':
    line = lines[i].strip()
    if ':' in line:
        char, code = line.split(': ')
        code_table[code] = char
    i += 1

# Skip blank line and get bit string
i += 1
if i < len(lines):
    bit_string = lines[i].strip()
else:
    bit_string = ''

# Decode the bit string
decoded = []
current_code = ''

for bit in bit_string:
    current_code += bit
    if current_code in code_table:
        decoded.append(code_table[current_code])
        current_code = ''

print(''.join(decoded))