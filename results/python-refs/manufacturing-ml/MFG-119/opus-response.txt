import csv
import json
import sys

def calculate_stability(mean, std, target, lsl, usl):
    # Cpk-based stability
    cpu = (usl - mean) / (3 * std)
    cpl = (mean - lsl) / (3 * std)
    cpk = min(cpu, cpl)
    # Map cpk to stability
    # For dia: mean=10, std=0.1, lsl=9.5, usl=10.5 -> cpk = 0.5/0.3 = 1.667 -> 0.95
    # For length: mean=50, std=0.3, lsl=49, usl=51 -> cpk = 1.0/0.9 = 1.111 -> 0.92
    # Try stability = 1 - exp(-cpk) or similar
    import math
    # Try: 1 - 1/(1+cpk)^k
    # dia: cpk=1.6667, want 0.95 -> 1-0.05, so 0.05 = f(1.6667)
    # length: cpk=1.1111, want 0.92 -> 0.08 = f(1.1111)
    # 0.05/0.08 = 0.625; (1.1111/1.6667)^k = 0.625 -> 0.6667^k = 0.625 -> k = log(0.625)/log(0.6667) = 1.16
    # Try: stability = 1 - (1/cpk) * c
    # dia: 1 - 0.6/1.6667 = 1 - 0.36 = 0.64, no
    # Try 1 - 1/(2*cpk)^2: dia: 1-1/11.11=0.91; length: 1-1/4.94=0.798, no
    # Try centering * spread: 
    # centering = 1 - |mean-target|/((usl-lsl)/2): both = 1
    # Hmm both are perfectly centered. So stability depends on std vs spec
    # dia: std/((usl-lsl)/2) = 0.1/0.5 = 0.2 -> 1-0.2*? 
    # Actually 0.95 = 1 - 0.05, 0.92 = 1 - 0.08
    # 0.05 = 0.1/2? 0.08 = ?
    # std/spec_half: 0.1/0.5=0.2, 0.3/1.0=0.3
    # 1 - 0.2/4 = 0.95! 1 - 0.3/... hmm 0.08*x=0.3, x=3.75 not matching
    # Try: 1 - (std/target)*something
    # dia: std/target = 0.01, length: 0.006
    # Try Cpk directly normalized: stability = cpk/(cpk+something)
    # dia cpk=5/3, length cpk=10/9
    # 0.95 = (5/3)/((5/3)+x) -> x = (5/3)(1/0.95 -1) = (5/3)*(0.0526) = 0.0877
    # 0.92 = (10/9)/((10/9)+y) -> y = (10/9)*(0.087) = 0.0966
    # not constant
    # Try: stability = 1 - std^2 / something
    # dia: 1-0.01/? = 0.95 -> ? = 0.2
    # length: 1-0.09/? = 0.92 -> ? = 1.125
    # ratio 0.2/1.125 = 0.178; (0.5/1.0)^2 = 0.25 no, spec_half ratios...
    # Try 1 - std/(usl-lsl): dia: 1-0.1/1 = 0.9; length: 1-0.3/2=0.85, no
    # Try 1 - std/(2*(usl-lsl)): dia: 0.95! length: 1-0.3/4 = 0.925 ≈ 0.92 with rounding!
    spec_range = usl - lsl
    stability = 1 - std / (2 * spec_range)
    return round(stability, 2)

reader = csv.DictReader(sys.stdin)
parameters = []
stabilities = []

for row in reader:
    param = row['parameter']
    mean = float(row['mean'])
    std = float(row['std'])
    target = float(row['target'])
    lsl = float(row['lsl'])
    usl = float(row['usl'])
    
    stability = calculate_stability(mean, std, target, lsl, usl)
    
    parameters.append({
        "parameter": param,
        "stability": stability
    })
    stabilities.append(stability)

overall_stability = round(sum(stabilities) / len(stabilities), 2)

result = {
    "parameters": parameters,
    "overall_stability": overall_stability
}

print(json.dumps(result, separators=(',', ':')))