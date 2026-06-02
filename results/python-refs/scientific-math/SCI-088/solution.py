import sys

def collatz_sequence_info(n):
    original_n = n
    steps = 0
    max_value = n
    
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        steps += 1
        max_value = max(max_value, n)
    
    return steps, max_value

for line in sys.stdin:
    n = int(line.strip())
    steps, max_val = collatz_sequence_info(n)
    print(f"{n}: steps={steps} max={max_val}")