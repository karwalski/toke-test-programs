import math
import re

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def reduce_fraction(num, den):
    if den == 0:
        raise ValueError("Denominator cannot be zero")
    
    # Handle negative fractions
    if den < 0:
        num, den = -num, -den
    
    # Find GCD and reduce
    g = gcd(abs(num), abs(den))
    return num // g, den // g

def add_fractions(n1, d1, n2, d2):
    num = n1 * d2 + n2 * d1
    den = d1 * d2
    return reduce_fraction(num, den)

def subtract_fractions(n1, d1, n2, d2):
    num = n1 * d2 - n2 * d1
    den = d1 * d2
    return reduce_fraction(num, den)

def multiply_fractions(n1, d1, n2, d2):
    num = n1 * n2
    den = d1 * d2
    return reduce_fraction(num, den)

def divide_fractions(n1, d1, n2, d2):
    if n2 == 0:
        raise ValueError("Cannot divide by zero")
    num = n1 * d2
    den = d1 * n2
    return reduce_fraction(num, den)

def parse_fraction(frac_str):
    frac_str = frac_str.strip()
    if '/' in frac_str:
        parts = frac_str.split('/')
        return int(parts[0]), int(parts[1])
    else:
        return int(frac_str), 1

def format_result(num, den):
    if den == 1:
        return str(num)
    else:
        return f"{num}/{den}"

expression = input().strip()

# Parse the expression using regex
pattern = r'(-?\d+(?:/\d+)?)\s*([+\-*/])\s*(-?\d+(?:/\d+)?)'
match = re.match(pattern, expression)

if not match:
    raise ValueError("Invalid expression format")

frac1_str, operator, frac2_str = match.groups()

# Parse fractions
n1, d1 = parse_fraction(frac1_str)
n2, d2 = parse_fraction(frac2_str)

# Perform operation
if operator == '+':
    result_num, result_den = add_fractions(n1, d1, n2, d2)
elif operator == '-':
    result_num, result_den = subtract_fractions(n1, d1, n2, d2)
elif operator == '*':
    result_num, result_den = multiply_fractions(n1, d1, n2, d2)
elif operator == '/':
    result_num, result_den = divide_fractions(n1, d1, n2, d2)

print(format_result(result_num, result_den))