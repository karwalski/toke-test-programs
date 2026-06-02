import sys
import json
import math

def main():
    line = sys.stdin.read().strip()
    data = [float(x) for x in line.split(',')]
    n = len(data)
    mean = sum(data) / n
    
    # Population variance/std
    m2 = sum((x - mean) ** 2 for x in data) / n
    std = math.sqrt(m2)
    
    if std == 0:
        skewness = 0.0
        kurtosis = 0.0
    else:
        # Population skewness
        skewness = sum(((x - mean) / std) ** 3 for x in data) / n
        # Population excess kurtosis
        kurtosis = sum(((x - mean) / std) ** 4 for x in data) / n - 3
    
    sk_r = round(skewness, 1)
    kt_r = round(kurtosis, 1)
    
    if abs(sk_r) < 1 and kt_r < 3:
        conclusion = "normal"
    else:
        conclusion = "not_normal"
    
    # Normalize -0.0 to 0.0
    if sk_r == 0:
        sk_r = 0.0
    
    result = {
        "skewness": sk_r,
        "kurtosis": kt_r,
        "conclusion": conclusion
    }
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()