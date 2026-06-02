import math

n = int(input())

if n <= 1:
    print("COMPOSITE")
elif n == 2:
    print("PRIME")
elif n % 2 == 0:
    print("COMPOSITE")
else:
    is_prime = True
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            is_prime = False
            break
    
    if is_prime:
        print("PRIME")
    else:
        print("COMPOSITE")