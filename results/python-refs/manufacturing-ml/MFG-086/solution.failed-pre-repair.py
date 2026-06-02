import sys
import json
import math
from scipy import stats

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    # Parse LSL and USL from first line
    lsl, usl = map(float, lines[0].split(','))
    
    # Parse measurements from second line
    measurements = list(map(float, lines[1].split(',')))
    
    # Calculate basic statistics
    n = len(measurements)
    mean = sum(measurements) / n
    
    # Calculate standard deviation (sample std)
    variance = sum((x - mean) ** 2 for x in measurements) / (n - 1)
    std = math.sqrt(variance)
    
    min_val = min(measurements)
    max_val = max(measurements)
    
    # Calculate Cp and Cpk
    cp = (usl - lsl) / (6 * std)
    cpk = min((usl - mean) / (3 * std), (mean - lsl) / (3 * std))
    
    # For Pp and Ppk, use population standard deviation
    pop_variance = sum((x - mean) ** 2 for x in measurements) / n
    pop_std = math.sqrt(pop_variance)
    
    pp = (usl - lsl) / (6 * pop_std)
    ppk = min((usl - mean) / (3 * pop_std), (mean - lsl) / (3 * pop_std))
    
    # Calculate PPM above and below limits
    # Using normal distribution approximation
    # PPM above USL
    z_upper = (usl - mean) / std
    ppm_above = int((1 - normal_cdf(z_upper)) * 1000000)
    
    # PPM below LSL
    z_lower = (lsl - mean) / std
    ppm_below = int(normal_cdf(z_lower) * 1000000)
    
    # Create output dictionary
    result = {
        "n": n,
        "mean": round(mean, 2),
        "std": round(std, 2),
        "min": min_val,
        "max": max_val,
        "cp": round(cp, 2),
        "cpk": round(cpk, 2),
        "pp": round(pp, 2),
        "ppk": round(ppk, 2),
        "ppm_above": ppm_above,
        "ppm_below": ppm_below
    }
    
    print(json.dumps(result, separators=(',', ':')))

def normal_cdf(z):
    """Approximation of normal cumulative distribution function"""
    return 0.5 * (1 + erf(z / math.sqrt(2)))

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

if __name__ == "__main__":
    main()