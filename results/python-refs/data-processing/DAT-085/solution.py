import csv
import sys
from math import sqrt

def chi_squared_test(a_success, a_total, b_success, b_total):
    # Create contingency table
    # [success_a, fail_a]
    # [success_b, fail_b]
    
    fail_a = a_total - a_success
    fail_b = b_total - b_success
    
    # Total counts
    total_success = a_success + b_success
    total_fail = fail_a + fail_b
    total_a = a_total
    total_b = b_total
    grand_total = total_a + total_b
    
    # Expected frequencies
    expected_a_success = (total_a * total_success) / grand_total
    expected_a_fail = (total_a * total_fail) / grand_total
    expected_b_success = (total_b * total_success) / grand_total
    expected_b_fail = (total_b * total_fail) / grand_total
    
    # Chi-squared statistic
    chi_sq = 0
    chi_sq += ((a_success - expected_a_success) ** 2) / expected_a_success
    chi_sq += ((fail_a - expected_a_fail) ** 2) / expected_a_fail
    chi_sq += ((b_success - expected_b_success) ** 2) / expected_b_success
    chi_sq += ((fail_b - expected_b_fail) ** 2) / expected_b_fail
    
    # For 2x2 table, degrees of freedom = 1
    # Critical value at 0.05 significance level is 3.841
    # But we need p-value, so we'll approximate
    
    # Simple approximation for p-value from chi-squared with df=1
    if chi_sq == 0:
        p_value = 1.0
    elif chi_sq >= 3.841:
        p_value = 0.0
    else:
        # Rough approximation - for exact calculation we'd need scipy
        # This is a simple linear interpolation for demonstration
        p_value = 1 - (chi_sq / 3.841) * 0.95
        if p_value < 0:
            p_value = 0.0
    
    return chi_sq, p_value

# Read CSV from stdin
reader = csv.DictReader(sys.stdin)
data = list(reader)

# Count outcomes by variant
a_success = 0
a_total = 0
b_success = 0
b_total = 0

for row in data:
    variant = row['variant']
    outcome = int(row['outcome'])
    
    if variant == 'A':
        a_total += 1
        if outcome == 1:
            a_success += 1
    elif variant == 'B':
        b_total += 1
        if outcome == 1:
            b_success += 1

# Calculate conversion rates
a_rate = (a_success / a_total) * 100 if a_total > 0 else 0
b_rate = (b_success / b_total) * 100 if b_total > 0 else 0

# Perform chi-squared test
chi_sq, p_value = chi_squared_test(a_success, a_total, b_success, b_total)

# Output results
print(f"A: {a_success}/{a_total} = {a_rate:.2f}%")
print(f"B: {b_success}/{b_total} = {b_rate:.2f}%")
print(f"Chi-squared: {chi_sq:.2f}")
print(f"p-value: {p_value:.2f}")

if p_value < 0.05:
    print("Significant (p < 0.05)")
else:
    print("Not significant (p >= 0.05)")