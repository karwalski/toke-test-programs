import sys, json, math

def erf(x):
    a1,a2,a3,a4,a5,p = 0.254829592,-0.284496736,1.421413741,-1.453152027,1.061405429,0.3275911
    sign = 1 if x >= 0 else -1
    x = abs(x)
    t = 1.0/(1.0+p*x)
    y = 1.0-(((((a5*t+a4)*t)+a3)*t+a2)*t+a1)*t*math.exp(-x*x)
    return sign*y

def ncdf(z):
    return 0.5*(1+erf(z/math.sqrt(2)))

def main():
    lines = [l.strip() for l in sys.stdin if l.strip()]
    lsl, usl = map(float, lines[0].split(','))
    measurements = list(map(float, lines[1].split(',')))
    n = len(measurements)
    mean = sum(measurements)/n
    variance = sum((x-mean)**2 for x in measurements)/(n-1)
    std = math.sqrt(variance)
    std_r = round(std, 2)
    min_val = min(measurements)
    max_val = max(measurements)
    cp = (usl-lsl)/(6*std_r)
    cpk = min((usl-mean)/(3*std_r), (mean-lsl)/(3*std_r))
    z_upper = (usl-mean)/std_r
    z_lower = (lsl-mean)/std_r
    ppm_above = int((1-ncdf(z_upper))*1000000)
    ppm_below = int(ncdf(z_lower)*1000000)
    result = {
        "n": n,
        "mean": round(mean,2),
        "std": std_r,
        "min": min_val,
        "max": max_val,
        "cp": round(cp,2),
        "cpk": round(cpk,2),
        "ppm_above": ppm_above,
        "ppm_below": ppm_below
    }
    print(json.dumps(result, separators=(',',':')))

main()