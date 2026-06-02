import sys

data = sys.stdin.read()
# Split on blank line
if '\n\n' in data:
    table_part, bit_part = data.split('\n\n', 1)
else:
    parts = data.split('\n\n', 1)
    table_part = parts[0]
    bit_part = parts[1] if len(parts) > 1 else ''

code_table = {}
for line in table_part.split('\n'):
    line = line.rstrip('\r')
    if not line.strip():
        continue
    if ':' in line:
        char, code = line.split(':', 1)
        code = code.strip()
        code_table[code] = char

bit_string = bit_part.strip().replace('\n', '').replace('\r', '')

decoded = []
current_code = ''
for bit in bit_string:
    current_code += bit
    if current_code in code_table:
        decoded.append(code_table[current_code])
        current_code = ''

if current_code != '':
    sys.stderr.write('Error: invalid bit string\n')
    sys.exit(1)

print(''.join(decoded))