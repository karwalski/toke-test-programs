import sys
import hashlib
import hmac
import time
import random

def string_compare_variable_time(secret, guess):
    """Variable-time string comparison - stops at first mismatch"""
    if len(secret) != len(guess):
        return False
    for i in range(len(secret)):
        if secret[i] != guess[i]:
            return False
    return True

def string_compare_constant_time(secret, guess):
    """Constant-time string comparison"""
    if len(secret) != len(guess):
        result = False
        # Still do work proportional to secret length
        for i in range(len(secret)):
            _ = secret[i]
    else:
        result = True
        for i in range(len(secret)):
            if secret[i] != guess[i]:
                result = False
    return result

def hash_compare_variable_time(secret, guess):
    """Variable-time hash comparison"""
    secret_hash = hashlib.sha256(secret.encode()).hexdigest()
    guess_hash = hashlib.sha256(guess.encode()).hexdigest()
    return string_compare_variable_time(secret_hash, guess_hash)

def hash_compare_constant_time(secret, guess):
    """Constant-time hash comparison"""
    secret_hash = hashlib.sha256(secret.encode()).hexdigest()
    guess_hash = hashlib.sha256(guess.encode()).hexdigest()
    return string_compare_constant_time(secret_hash, guess_hash)

def hmac_verify_variable_time(secret, guess):
    """Variable-time HMAC verification"""
    key = b"fixed_key_for_demo"
    secret_hmac = hmac.new(key, secret.encode(), hashlib.sha256).hexdigest()
    guess_hmac = hmac.new(key, guess.encode(), hashlib.sha256).hexdigest()
    return string_compare_variable_time(secret_hmac, guess_hmac)

def hmac_verify_constant_time(secret, guess):
    """Constant-time HMAC verification"""
    key = b"fixed_key_for_demo"
    secret_hmac = hmac.new(key, secret.encode(), hashlib.sha256).hexdigest()
    guess_hmac = hmac.new(key, guess.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(secret_hmac, guess_hmac)

def simulate_timing(func, secret, guess):
    """Simulate timing measurements with realistic variations"""
    # Base timing simulation
    base_time = 1000000  # 1ms in nanoseconds
    
    # Add randomness
    jitter = random.randint(-100000, 100000)
    
    # Simulate variable timing based on how much work is done
    if func.__name__.endswith('variable_time'):
        # For variable time, timing depends on how much of the comparison is done
        if 'string_compare' in func.__name__:
            min_len = min(len(secret), len(guess))
            matching_chars = 0
            for i in range(min_len):
                if secret[i] == guess[i]:
                    matching_chars += 1
                else:
                    break
            # More matching characters = more time spent
            work_time = matching_chars * 50000  # 50μs per character
        else:
            # For hash/hmac, the work is in the comparison of the hashes
            work_time = base_time // 2
    else:
        # Constant time always does full work
        work_time = len(secret) * 50000
    
    total_time = base_time + work_time + jitter
    return max(total_time, 100000)  # Minimum 100μs

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    function_type = lines[0]
    secret = lines[1]
    guesses = lines[2:]
    
    # Select functions based on type
    if function_type == 'string_compare':
        var_func = string_compare_variable_time
        const_func = string_compare_constant_time
    elif function_type == 'hash_compare':
        var_func = hash_compare_variable_time
        const_func = hash_compare_constant_time
    elif function_type == 'hmac_verify':
        var_func = hmac_verify_variable_time
        const_func = hmac_verify_constant_time
    
    # Set random seed for reproducible timing simulation
    random.seed(42)
    
    results = []
    
    # Process each guess
    for guess in guesses:
        # Use variable-time function for timing simulation
        timing_ns = simulate_timing(var_func, secret, guess)
        correctly_rejected = guess != secret
        
        results.append((timing_ns, correctly_rejected))
        print(f"{timing_ns}, {correctly_rejected}")
    
    # Print timing chart
    print("\nTiming Analysis:")
    print("Guess".ljust(15), "Timing (ns)".ljust(12), "Rejected")
    print("-" * 40)
    
    for i, guess in enumerate(guesses):
        timing, rejected = results[i]
        print(f"{guess}".ljust(15), f"{timing}".ljust(12), rejected)

if __name__ == "__main__":
    main()