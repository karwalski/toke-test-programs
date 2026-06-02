import math

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def euler_totient(n):
    if n == 1:
        return 1
    
    count = 0
    for i in range(1, n + 1):
        if gcd(i, n) == 1:
            count += 1
    
    return count

n = int(input())
print(euler_totient(n))