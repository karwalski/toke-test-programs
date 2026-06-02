import sys

def npv(rate, cash_flows):
    """Calculate Net Present Value for given rate and cash flows"""
    return sum(cf / (1 + rate) ** i for i, cf in enumerate(cash_flows))

def npv_derivative(rate, cash_flows):
    """Calculate derivative of NPV with respect to rate"""
    return sum(-i * cf / (1 + rate) ** (i + 1) for i, cf in enumerate(cash_flows))

def irr_newton(cash_flows, initial_guess=0.1, tolerance=1e-8, max_iterations=100):
    """Calculate IRR using Newton's method"""
    rate = initial_guess
    
    for _ in range(max_iterations):
        npv_val = npv(rate, cash_flows)
        npv_deriv = npv_derivative(rate, cash_flows)
        
        if abs(npv_val) < tolerance:
            break
            
        if abs(npv_deriv) < tolerance:
            # Avoid division by zero
            break
            
        rate = rate - npv_val / npv_deriv
    
    return rate

# Read input
input_line = input().strip()
cash_flows = [float(x) for x in input_line.split(',')]

# Calculate IRR
irr = irr_newton(cash_flows)

# Convert to percentage and format to 2 decimal places
irr_percentage = irr * 100
print(f"{irr_percentage:.2f}%")