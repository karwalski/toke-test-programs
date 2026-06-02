import sys
import math

def read_samples():
    line1 = input().strip()
    line2 = input().strip()
    
    sample1 = [float(x) for x in line1.split(',')]
    sample2 = [float(x) for x in line2.split(',')]
    
    return sample1, sample2

def mean(data):
    return sum(data) / len(data)

def variance(data):
    m = mean(data)
    return sum((x - m) ** 2 for x in data) / (len(data) - 1)

def two_sample_t_test(sample1, sample2):
    n1 = len(sample1)
    n2 = len(sample2)
    
    mean1 = mean(sample1)
    mean2 = mean(sample2)
    
    var1 = variance(sample1)
    var2 = variance(sample2)
    
    # Pooled standard error
    pooled_se = math.sqrt(var1/n1 + var2/n2)
    
    # t-statistic
    t_stat = (mean1 - mean2) / pooled_se
    
    return t_stat

# Read input
sample1, sample2 = read_samples()

# Calculate t-statistic
t_statistic = two_sample_t_test(sample1, sample2)

# Output result to 4 decimal places
print(f"{t_statistic:.4f}")