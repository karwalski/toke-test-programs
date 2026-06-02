import sys
import cmath

def evaluate_polynomial(coeffs, x):
    """Evaluate polynomial at point x using Horner's method"""
    result = 0
    for coeff in coeffs:
        result = result * x + coeff
    return result

def durand_kerner(coeffs, max_iterations, tolerance):
    """Find all roots of polynomial using Durand-Kerner method"""
    n = len(coeffs) - 1  # degree of polynomial
    
    if n == 0:
        return []
    
    # Initialize roots with well-separated complex numbers
    roots = []
    for k in range(n):
        angle = 2 * cmath.pi * k / n
        # Use radius slightly larger than 1 to avoid clustering
        radius = 0.4 + 0.9 * cmath.exp(1j * angle)
        roots.append(radius)
    
    # Durand-Kerner iteration
    for iteration in range(max_iterations):
        new_roots = []
        max_change = 0
        
        for i in range(n):
            # Calculate polynomial value at current root
            p_value = evaluate_polynomial(coeffs, roots[i])
            
            # Calculate denominator (product of differences)
            denominator = 1
            for j in range(n):
                if i != j:
                    denominator *= (roots[i] - roots[j])
            
            if abs(denominator) < 1e-15:
                # Avoid division by very small numbers
                new_root = roots[i]
            else:
                # Update root using Durand-Kerner formula
                new_root = roots[i] - p_value / denominator
            
            change = abs(new_root - roots[i])
            max_change = max(max_change, change)
            new_roots.append(new_root)
        
        roots = new_roots
        
        # Check convergence
        if max_change < tolerance:
            break
    
    return roots

def main():
    # Read input
    coeffs_line = input().strip()
    coeffs = [float(x) for x in coeffs_line.split()]
    max_iterations = int(input().strip())
    tolerance = float(input().strip())
    
    # Find roots
    roots = durand_kerner(coeffs, max_iterations, tolerance)
    
    # Sort roots by real part
    roots.sort(key=lambda x: x.real)
    
    # Output results
    for i, root in enumerate(roots):
        real_part = root.real
        imag_part = root.imag
        
        # Format with 6 decimal places
        if imag_part >= 0:
            print(f"Root {i+1}: {real_part:.6f}+{imag_part:.6f}i")
        else:
            print(f"Root {i+1}: {real_part:.6f}{imag_part:.6f}i")

if __name__ == "__main__":
    main()