import math

# Read input
N = int(input())
x = list(map(float, input().split()))

# Compute DFT using direct formula
X = []
for k in range(N):
    real_part = 0
    imag_part = 0
    for n in range(N):
        angle = -2 * math.pi * k * n / N
        real_part += x[n] * math.cos(angle)
        imag_part += x[n] * math.sin(angle)
    
    # Compute magnitude
    magnitude = math.sqrt(real_part * real_part + imag_part * imag_part)
    X.append(magnitude)

# Output magnitudes with 4 decimal places
print("Magnitudes:", " ".join(f"{mag:.4f}" for mag in X))