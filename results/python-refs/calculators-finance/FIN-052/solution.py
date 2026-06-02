import sys

# Read input and parse numbers
line = input().strip()
numbers = [float(x) for x in line.split(',')]
numbers.sort()

n = len(numbers)

# Calculate min and max
min_val = numbers[0]
max_val = numbers[-1]

# Calculate median
if n % 2 == 0:
    median = (numbers[n//2 - 1] + numbers[n//2]) / 2
else:
    median = numbers[n//2]

# Calculate Q1 (median of lower half)
lower_half = numbers[:n//2]
if len(lower_half) % 2 == 0:
    q1 = (lower_half[len(lower_half)//2 - 1] + lower_half[len(lower_half)//2]) / 2
else:
    q1 = lower_half[len(lower_half)//2]

# Calculate Q3 (median of upper half)
if n % 2 == 0:
    upper_half = numbers[n//2:]
else:
    upper_half = numbers[n//2 + 1:]

if len(upper_half) % 2 == 0:
    q3 = (upper_half[len(upper_half)//2 - 1] + upper_half[len(upper_half)//2]) / 2
else:
    q3 = upper_half[len(upper_half)//2]

# Format output - remove .0 for whole numbers
def format_num(x):
    if x == int(x):
        return str(int(x))
    else:
        return str(x)

print(format_num(min_val), format_num(q1), format_num(median), format_num(q3), format_num(max_val))