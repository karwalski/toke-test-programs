def is_armstrong(n):
    str_n = str(n)
    num_digits = len(str_n)
    digit_sum = sum(int(digit) ** num_digits for digit in str_n)
    return digit_sum == n

D = int(input())

# Find all Armstrong numbers with at most D digits
armstrong_numbers = []

# Check numbers from 1 to 10^D - 1 (numbers with at most D digits)
for i in range(1, 10**D):
    if is_armstrong(i):
        armstrong_numbers.append(i)

# Output each Armstrong number on a separate line
for num in armstrong_numbers:
    print(num)