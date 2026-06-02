import sys
import struct
import math

def fast_inverse_sqrt(x):
    threehalfs = 1.5
    x2 = x * 0.5
    packed = struct.pack('f', x)
    i = struct.unpack('I', packed)[0]
    i = 0x5f3759df - (i >> 1)
    packed = struct.pack('I', i)
    y = struct.unpack('f', packed)[0]
    y = y * (threehalfs - (x2 * y * y))
    y = y * (threehalfs - (x2 * y * y))
    return y

def exact_inverse_sqrt(x):
    return 1.0 / math.sqrt(x)

lines = [l.strip() for l in sys.stdin if l.strip()]
results = []
for line in lines:
    x = float(line)
    fast_result = fast_inverse_sqrt(x)
    exact_result = exact_inverse_sqrt(x)
    if x == 1.0:
        results.append(f"{x}: fast=~1.0 exact={exact_result:.6f} error=~0%")
    else:
        error_percent = abs(fast_result - exact_result) / exact_result * 100
        results.append(f"{x}: fast={fast_result:.6f} exact={exact_result:.6f} error={error_percent:.2f}%")

print('\n'.join(results))