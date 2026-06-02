import sys

for line in sys.stdin:
    snake_case = line.strip()
    if snake_case:
        parts = snake_case.split('_')
        camel_case = parts[0] + ''.join(word.capitalize() for word in parts[1:])
        print(camel_case)