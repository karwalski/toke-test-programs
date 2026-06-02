import math

def fft(x):
    N = len(x)
    if N <= 1:
        return x
    
    # Divide
    even = fft([x[i] for i in range(0, N, 2)])
    odd = fft([x[i] for i in range(1, N, 2)])
    
    # Combine
    result = [0] * N
    for k in range(N // 2):
        t = complex(math.cos(-2 * math.pi * k / N), math.sin(-2 * math.pi * k / N)) * odd[k]
        result[k] = even[k] + t
        result[k + N // 2] = even[k] - t
    
    return result

# Read input
N = int(input())
numbers = list(map(float, input().split()))

# Convert to complex numbers
x = [complex(num, 0) for num in numbers]

# Compute FFT
result = fft(x)

# Output results
for coeff in result:
    print(f"{coeff.real} {coeff.imag}")