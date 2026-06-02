import random
import string
import sys

# Read input
type_input = input().strip()
count_or_length = int(input().strip())

if type_input in ['int', 'float']:
    range_line = input().strip().split()
    min_val = float(range_line[0]) if type_input == 'float' else int(range_line[0])
    max_val = float(range_line[1]) if type_input == 'float' else int(range_line[1])

# Generate output based on type
if type_input == 'bytes':
    for _ in range(count_or_length):
        byte_val = random.randint(0, 255)
        print(byte_val)
elif type_input == 'int':
    for _ in range(count_or_length):
        value = random.randint(min_val, max_val)
        print(value)
elif type_input == 'float':
    for _ in range(count_or_length):
        value = random.uniform(min_val, max_val)
        print(value)
elif type_input == 'string':
    chars = string.ascii_letters + string.digits
    for _ in range(count_or_length):
        random_string = ''.join(random.choice(chars) for _ in range(count_or_length))
        print(random_string)