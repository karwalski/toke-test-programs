import sys
import struct
import math

def fast_inverse_sqrt(x):
    # Convert float to 32-bit integer representation
    packed = struct.pack('f', x)
    i = struct.unpack('I', packed)[0]
    
    # Magic number and bit manipulation
    i = 0x5f3759df - (i >> 1)
    
    # Convert back to float
    packed = struct.pack('I', i)
    y = struct.unpack('f', packed)[0]
    
    # Newton-Raphson iteration
    y = y * (1.5 - 0.5 * x * y * y)
    
    return y

def exact_inverse_sqrt(x):
    return 1.0 / math.sqrt(x)

# Read input and process
for line in sys.stdin:
    x = float(line.strip())
    
    fast_result = fast_inverse_sqrt(x)
    exact_result = exact_inverse_sqrt(x)
    
    error_percent = abs(fast_result - exact_result) / exact_result * 100
    
    print(f"{x}: fast={fast_result:.6f} exact={exact_result:.6f} error={error_percent:.2f}%")