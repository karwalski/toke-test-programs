import json
import sys
import math

def read_input():
    return json.loads(sys.stdin.read().strip())

def z_test_two_proportions(p1, n1, p2, n2):
    """Perform two-proportion z-test"""
    if n1 == 0 or n2 == 0:
        return 0, 1
    
    # Pool the proportions
    p_pool = (p1 * n1 + p2 * n2) / (n1 + n2)
    
    # Standard error
    se = math.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
    
    if se == 0:
        return 0, 1
    
    # Z statistic
    z = (p2 - p1) / se
    
    # Two-tailed p-value using normal approximation
    p_value = 2 * (1 - normal_cdf(abs(z)))
    
    return z, p_value

def normal_cdf(x):
    """Approximation of normal CDF using error function approximation"""
    return 0.5 * (1 + erf(x / math.sqrt(2)))

def erf(x):
    """Approximation of error function"""
    # Abramowitz and Stegun approximation
    a1 =  0.254829592
    a2 = -0.284496736
    a3 =  1.421413741
    a4 = -1.453152027
    a5 =  1.061405429
    p  =  0.3275911
    
    sign = 1 if x >= 0 else -1
    x = abs(x)
    
    t = 1.0 / (1.0 + p * x)
    y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-x * x)
    
    return sign * y

def solve_ab_test(data):
    variant_a = data['variant_a']
    variant_b = data['variant_b']
    confidence_level = data['confidence_level']
    
    # Calculate success rates
    rate_a = variant_a['successes'] / variant_a['total']
    rate_b = variant_b['successes'] / variant_b['total']
    
    # Perform statistical test
    z_stat, p_value = z_test_two_proportions(
        rate_a, variant_a['total'],
        rate_b, variant_b['total']
    )
    
    # Determine significance
    alpha = 1 - confidence_level
    significant = p_value < alpha
    
    # Determine winner
    if not significant:
        winner = "inconclusive"
    elif rate_b > rate_a:
        winner = "b"
    elif rate_a > rate_b:
        winner = "a"
    else:
        winner = "inconclusive"
    
    # Calculate lift percentage
    if rate_a == 0:
        lift_pct = 0 if rate_b == 0 else float('inf')
    else:
        lift_pct = ((rate_b - rate_a) / rate_a) * 100
    
    # Round to reasonable precision
    if lift_pct != float('inf'):
        lift_pct = round(lift_pct, 1)
    
    return {
        "winner": winner,
        "rate_a": rate_a,
        "rate_b": rate_b,
        "significant": significant,
        "lift_pct": lift_pct
    }

def main():
    data = read_input()
    result = solve_ab_test(data)
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()