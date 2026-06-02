import sys
from math import gcd
from functools import reduce

def euclidean_gcd_with_steps(a, b):
    steps = []
    original_a, original_b = a, b
    
    while b != 0:
        steps.append(f"gcd({a},{b})")
        a, b = b, a % b
    
    steps.append(f"gcd({a},0)={a}")
    return a, steps

def gcd_multiple(numbers):
    return reduce(gcd, numbers)

def lcm_two(a, b):
    return abs(a * b) // gcd(a, b)

def lcm_multiple(numbers):
    return reduce(lcm_two, numbers)

# Read input
mode = input().strip()
numbers = list(map(int, input().split()))

# Calculate GCD and LCM
gcd_result = gcd_multiple(numbers)
lcm_result = lcm_multiple(numbers)

# Output based on mode
if mode == "gcd":
    print(f"GCD: {gcd_result}")
elif mode == "lcm":
    print(f"LCM: {lcm_result}")
elif mode == "both":
    print(f"GCD: {gcd_result} LCM: {lcm_result}")

# Show steps for Euclidean algorithm (only for first two numbers)
if len(numbers) >= 2:
    a, b = numbers[0], numbers[1]
    if a < b:
        a, b = b, a
    _, steps = euclidean_gcd_with_steps(a, b)
    print("Steps: " + " ".join(steps))