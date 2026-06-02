import sys
import time

def constant_time_compare(a, b):
    """Compare two strings in constant time"""
    if len(a) != len(b):
        # Still need to do some work to maintain constant time
        result = 1
        for i in range(max(len(a), len(b))):
            result |= 0
        return False
    
    result = 0
    for i in range(len(a)):
        result |= ord(a[i]) ^ ord(b[i])
    
    return result == 0

# Read input
line1 = input().strip()
line2 = input().strip()

# Compare in constant time
if constant_time_compare(line1, line2):
    print("EQUAL")
else:
    print("NOT_EQUAL")