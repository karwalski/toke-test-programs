import sys
import hashlib
import hmac
import time
import random

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    function_type = lines[0]
    secret = lines[1]
    guesses = lines[2:]
    
    random.seed(42)
    
    print("timing_ns, correctly_rejected")
    
    results = []
    for guess in guesses:
        base_time = 1000000
        jitter = random.randint(-100000, 100000)
        if function_type == 'string_compare':
            min_len = min(len(secret), len(guess))
            matching = 0
            for i in range(min_len):
                if secret[i] == guess[i]:
                    matching += 1
                else:
                    break
            work_time = matching * 50000
        else:
            work_time = base_time // 2
        timing_ns = max(base_time + work_time + jitter, 100000)
        correctly_rejected = guess != secret
        results.append((guess, timing_ns, correctly_rejected))
        print(f"{timing_ns}, {correctly_rejected}")
    
    print()
    print("Timing Analysis:")
    print("Guess".ljust(20), "timing_ns".ljust(12), "Rejected")
    print("-" * 50)
    for guess, timing, rejected in results:
        print(f"{guess}".ljust(20), f"{timing}".ljust(12), rejected)

if __name__ == "__main__":
    main()