import sys
import json
import math
from collections import defaultdict

def get_first_digit(num):
    """Extract the first digit from a number"""
    num_str = str(abs(float(num))).replace('.', '')
    for char in num_str:
        if char.isdigit() and char != '0':
            return int(char)
    return None

def benford_expected():
    """Return expected frequencies according to Benford's law"""
    expected = {}
    for d in range(1, 10):
        expected[str(d)] = math.log10(1 + 1/d)
    return expected

def calculate_chi_squared(observed, expected, total_count):
    """Calculate chi-squared statistic"""
    chi_sq = 0
    for digit in range(1, 10):
        digit_str = str(digit)
        obs_count = observed.get(digit_str, 0) * total_count
        exp_count = expected[digit_str] * total_count
        if exp_count > 0:
            chi_sq += ((obs_count - exp_count) ** 2) / exp_count
    return chi_sq

def main():
    # Read input from stdin
    lines = []
    for line in sys.stdin:
        line = line.strip()
        if line and line != 'value':  # Skip header
            lines.append(line)
    
    # Count first digits
    digit_counts = defaultdict(int)
    total_valid = 0
    
    for line in lines:
        try:
            first_digit = get_first_digit(float(line))
            if first_digit:
                digit_counts[str(first_digit)] += 1
                total_valid += 1
        except ValueError:
            continue
    
    if total_valid == 0:
        print('{"observed":{},"chi_squared":0,"suspicious":false}')
        return
    
    # Calculate observed frequencies
    observed = {}
    for digit_str, count in digit_counts.items():
        freq = count / total_valid
        observed[digit_str] = round(freq, 1)
    
    # Get expected frequencies from Benford's law
    expected = benford_expected()
    
    # Calculate chi-squared
    chi_sq = calculate_chi_squared(observed, expected, total_valid)
    
    # Determine if suspicious (chi-squared > critical value)
    # For 8 degrees of freedom at 0.05 significance level, critical value is ~15.51
    suspicious = chi_sq > 15.51
    
    # Format output
    result = {
        "observed": observed,
        "chi_squared": round(chi_sq, 1),
        "suspicious": suspicious
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()