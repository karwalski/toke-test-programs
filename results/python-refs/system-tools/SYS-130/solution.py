#!/usr/bin/env python3

import os

def read_entropy_info():
    try:
        # Read entropy available from /proc/sys/kernel/random/entropy_avail
        with open('/proc/sys/kernel/random/entropy_avail', 'r') as f:
            entropy_available = int(f.read().strip())
    except:
        entropy_available = 0
    
    try:
        # Read entropy pool size from /proc/sys/kernel/random/poolsize
        with open('/proc/sys/kernel/random/poolsize', 'r') as f:
            entropy_pool = int(f.read().strip())
    except:
        entropy_pool = 0
    
    return entropy_available, entropy_pool

def main():
    entropy_available, entropy_pool = read_entropy_info()
    
    print(f"Entropy available: {entropy_available} bits")
    print(f"Entropy pool: {entropy_pool} bits")
    
    if entropy_available < 256:
        print("WARNING: low entropy")

if __name__ == "__main__":
    main()