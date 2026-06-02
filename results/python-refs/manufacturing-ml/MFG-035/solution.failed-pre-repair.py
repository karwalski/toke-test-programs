import csv
import sys
import json
import math

def read_data():
    reader = csv.DictReader(sys.stdin)
    data = []
    for row in reader:
        data.append(float(row['time_to_failure']))
    return data

def weibull_mle(data):
    # Maximum likelihood estimation for Weibull parameters
    n = len(data)
    
    # Initial guess for beta
    beta = 1.0
    
    # Iterative solution for beta using Newton-Raphson method
    for _ in range(100):  # Max iterations
        sum_ln_t = sum(math.log(t) for t in data)
        sum_t_beta_ln_t = sum(t**beta * math.log(t) for t in data)
        sum_t_beta = sum(t**beta for t in data)
        
        # First derivative
        f1 = n / beta + sum_ln_t - n * sum_t_beta_ln_t / sum_t_beta
        
        # Second derivative (approximation for stability)
        f2 = -n / (beta**2) - n * (sum_t_beta_ln_t / sum_t_beta)**2
        
        if abs(f1) < 1e-6:
            break
            
        beta_new = beta - f1 / f2
        if beta_new <= 0:
            beta_new = beta / 2
            
        if abs(beta_new - beta) < 1e-6:
            break
            
        beta = beta_new
    
    # Calculate eta (scale parameter)
    eta = (sum(t**beta for t in data) / n)**(1/beta)
    
    return beta, eta

def gamma_function(x):
    # Stirling's approximation for gamma function
    if x == 1:
        return 1
    return math.sqrt(2 * math.pi / x) * (x / math.e)**x

def weibull_mean(beta, eta):
    # Mean = eta * Gamma(1 + 1/beta)
    gamma_arg = 1 + 1/beta
    
    # Use built-in math.gamma if available, otherwise approximation
    try:
        return eta * math.gamma(gamma_arg)
    except:
        # Simple approximation for common cases
        if abs(gamma_arg - 1.333) < 0.1:  # around beta=3
            gamma_val = 0.893
        else:
            gamma_val = 0.9
        return eta * gamma_val

def weibull_reliability(t, beta, eta):
    # R(t) = exp(-(t/eta)^beta)
    return math.exp(-((t/eta)**beta))

def main():
    data = read_data()
    
    beta, eta = weibull_mle(data)
    mean_life = weibull_mean(beta, eta)
    reliability_200 = weibull_reliability(200, beta, eta)
    
    result = {
        "beta": round(beta, 2),
        "eta": round(eta, 1),
        "mean_life": round(mean_life, 1),
        "reliability_at_200": round(reliability_200, 2)
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()