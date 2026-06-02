import sys
import json
import math
from collections import Counter

def calculate_entropy(data):
    """Calculate Shannon entropy per bit"""
    if not data:
        return 0
    
    # Count frequency of each byte value
    counts = Counter(data)
    length = len(data)
    
    # Calculate entropy
    entropy = 0
    for count in counts.values():
        probability = count / length
        if probability > 0:
            entropy -= probability * math.log2(probability)
    
    return entropy

def frequency_test(data):
    """Frequency test - check if distribution is roughly uniform"""
    if not data:
        return False
    
    counts = Counter(data)
    expected = len(data) / 256  # Expected count for uniform distribution
    
    # Allow some tolerance - within 20% of expected for reasonable uniformity
    tolerance = 0.2 * expected if expected > 0 else 1
    
    for value in range(256):
        count = counts.get(value, 0)
        if abs(count - expected) > tolerance and len(data) > 100:
            return False
    
    return True

def runs_test(data):
    """Runs test - check for independence between consecutive bits"""
    if len(data) < 2:
        return True
    
    # Convert bytes to bits
    bits = []
    for byte in data:
        for i in range(8):
            bits.append((byte >> i) & 1)
    
    if len(bits) < 20:
        return True
    
    # Count runs (consecutive identical bits)
    runs = 1
    for i in range(1, len(bits)):
        if bits[i] != bits[i-1]:
            runs += 1
    
    n = len(bits)
    ones = sum(bits)
    zeros = n - ones
    
    # Expected number of runs
    expected_runs = (2 * ones * zeros / n) + 1
    
    # Variance of runs
    variance = (2 * ones * zeros * (2 * ones * zeros - n)) / (n * n * (n - 1))
    
    if variance <= 0:
        return True
    
    # Z-score
    z = abs(runs - expected_runs) / math.sqrt(variance)
    
    # Pass if z-score is reasonable (< 2 for ~95% confidence)
    return z < 2.0

def chi_square_test(data):
    """Chi-square test for uniformity"""
    if not data:
        return False
    
    counts = Counter(data)
    expected = len(data) / 256
    
    if expected < 5:  # Not enough data for reliable chi-square test
        return True
    
    chi_square = 0
    for value in range(256):
        observed = counts.get(value, 0)
        chi_square += ((observed - expected) ** 2) / expected
    
    # Critical value for 255 degrees of freedom at 0.05 significance level
    # Using approximation for large df: critical ≈ df + sqrt(2*df) * 1.645
    critical_value = 255 + math.sqrt(2 * 255) * 1.645
    
    return chi_square < critical_value

def assess_quality(data):
    """Assess overall randomness quality"""
    if not data:
        return "poor"
    
    entropy = calculate_entropy(data)
    freq_pass = frequency_test(data)
    runs_pass = runs_test(data)
    chi_pass = chi_square_test(data)
    
    # Quality assessment based on multiple criteria
    tests_passed = sum([freq_pass, runs_pass, chi_pass])
    
    # High entropy (close to 8 bits per byte) is good
    entropy_good = entropy > 7.5
    
    if entropy_good and tests_passed >= 2:
        return "good"
    elif entropy > 6.0 and tests_passed >= 1:
        return "fair"
    else:
        return "poor"

def main():
    # Read input
    n = int(input().strip())
    hex_data = input().strip()
    
    # Convert hex to bytes
    try:
        data = bytes.fromhex(hex_data)
    except ValueError:
        print("poor")
        return
    
    # Verify we got the expected number of bytes
    if len(data) != n:
        print("poor")
        return
    
    # Assess quality
    quality = assess_quality(data)
    print(quality)

if __name__ == "__main__":
    main()