import math

def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)

def lcm_multiple(numbers):
    result = numbers[0]
    for i in range(1, len(numbers)):
        result = lcm(result, numbers[i])
    return result

input_line = input().strip()
numbers = [int(x.strip()) for x in input_line.split(',')]

result = lcm_multiple(numbers)
print(result)