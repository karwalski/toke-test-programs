import sys

def int_to_roman(num):
    values = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    symbols = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    
    result = ""
    for i in range(len(values)):
        count = num // values[i]
        result += symbols[i] * count
        num -= values[i] * count
    return result

def roman_to_int(roman):
    values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    
    total = 0
    prev_value = 0
    
    for char in reversed(roman):
        value = values[char]
        if value < prev_value:
            total -= value
        else:
            total += value
        prev_value = value
    
    return total

for line in sys.stdin:
    line = line.strip()
    if line.isdigit():
        print(int_to_roman(int(line)))
    else:
        print(roman_to_int(line))