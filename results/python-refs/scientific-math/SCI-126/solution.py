import sys
import math

def haar_forward(signal):
    n = len(signal)
    result = signal[:]
    
    while n > 1:
        temp = [0] * n
        half = n // 2
        
        # Compute averages (scaling coefficients)
        for i in range(half):
            temp[i] = (result[2*i] + result[2*i + 1]) / math.sqrt(2)
        
        # Compute differences (wavelet coefficients)
        for i in range(half):
            temp[half + i] = (result[2*i] - result[2*i + 1]) / math.sqrt(2)
        
        # Copy back
        for i in range(n):
            result[i] = temp[i]
        
        n = half
    
    return result

def haar_inverse(coeffs):
    n = len(coeffs)
    result = coeffs[:]
    
    length = 1
    while length < n:
        temp = [0] * (2 * length)
        
        # Reconstruct from scaling and wavelet coefficients
        for i in range(length):
            avg = result[i]
            diff = result[length + i]
            
            temp[2*i] = (avg + diff) / math.sqrt(2)
            temp[2*i + 1] = (avg - diff) / math.sqrt(2)
        
        # Copy back
        for i in range(2 * length):
            result[i] = temp[i]
        
        length *= 2
    
    return result

# Read input
mode = input().strip()
n = int(input().strip())
values = list(map(float, input().strip().split()))

# Apply transformation
if mode == "forward":
    result = haar_forward(values)
else:  # inverse
    result = haar_inverse(values)

# Output with 6 decimal places
print(" ".join(f"{x:.6f}" for x in result))