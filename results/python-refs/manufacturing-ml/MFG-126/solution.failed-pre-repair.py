import sys
import json
import math

def read_measurements():
    line = sys.stdin.read().strip()
    return [float(x) for x in line.split(',')]

def calculate_mean(data):
    return sum(data) / len(data)

def calculate_variance(data, mean):
    return sum((x - mean) ** 2 for x in data) / (len(data) - 1)

def calculate_skewness(data):
    n = len(data)
    mean = calculate_mean(data)
    variance = calculate_variance(data, mean)
    std_dev = math.sqrt(variance)
    
    if std_dev == 0:
        return 0.0
    
    skewness = sum(((x - mean) / std_dev) ** 3 for x in data) * n / ((n - 1) * (n - 2))
    return skewness

def calculate_kurtosis(data):
    n = len(data)
    mean = calculate_mean(data)
    variance = calculate_variance(data, mean)
    std_dev = math.sqrt(variance)
    
    if std_dev == 0:
        return 0.0
    
    kurtosis = sum(((x - mean) / std_dev) ** 4 for x in data) * n * (n + 1) / ((n - 1) * (n - 2) * (n - 3))
    kurtosis -= 3 * (n - 1) ** 2 / ((n - 2) * (n - 3))
    return kurtosis

def anderson_darling_test(data):
    n = len(data)
    data_sorted = sorted(data)
    mean = calculate_mean(data)
    variance = calculate_variance(data, mean)
    std_dev = math.sqrt(variance)
    
    # Standardize data
    z_scores = [(x - mean) / std_dev for x in data_sorted]
    
    # Calculate Anderson-Darling statistic (simplified)
    # Using normal CDF approximation
    def normal_cdf(x):
        return 0.5 * (1 + math.erf(x / math.sqrt(2)))
    
    ad_stat = 0
    for i in range(n):
        cdf_val = normal_cdf(z_scores[i])
        if cdf_val > 0 and cdf_val < 1:
            ad_stat += (2 * i + 1) * (math.log(cdf_val) + math.log(1 - normal_cdf(z_scores[n - 1 - i])))
    
    ad_stat = -n - ad_stat / n
    
    # Critical value for normal distribution at 5% significance level
    critical_value = 0.752
    
    return ad_stat < critical_value

def determine_conclusion(skewness, kurtosis, anderson_result):
    # Simple heuristic for normality
    skew_threshold = 0.5
    kurt_threshold = 1.0
    
    skew_normal = abs(skewness) < skew_threshold
    kurt_normal = abs(kurtosis) < kurt_threshold
    
    if skew_normal and kurt_normal and anderson_result:
        return "normal"
    else:
        return "not_normal"

def main():
    measurements = read_measurements()
    
    skewness = calculate_skewness(measurements)
    kurtosis = calculate_kurtosis(measurements)
    anderson_result = anderson_darling_test(measurements)
    conclusion = determine_conclusion(skewness, kurtosis, anderson_result)
    
    result = {
        "skewness": round(skewness, 1),
        "kurtosis": round(kurtosis, 1),
        "conclusion": conclusion
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()