import sys

def main():
    # Read input lines
    lines = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            lines.append(line)
    
    # Parse returns for each asset
    assets = []
    for line in lines:
        returns = [float(x) for x in line.split(',')]
        assets.append(returns)
    
    n_assets = len(assets)
    n_periods = len(assets[0])
    
    # Calculate means for each asset
    means = []
    for asset in assets:
        mean = sum(asset) / n_periods
        means.append(mean)
    
    # Calculate covariance matrix
    cov_matrix = []
    for i in range(n_assets):
        row = []
        for j in range(n_assets):
            # Calculate covariance between asset i and asset j
            cov = 0.0
            for k in range(n_periods):
                cov += (assets[i][k] - means[i]) * (assets[j][k] - means[j])
            cov = cov / (n_periods - 1)  # Sample covariance (n-1 denominator)
            row.append(cov)
        cov_matrix.append(row)
    
    # Output covariance matrix
    for i in range(n_assets):
        row_str = []
        for j in range(n_assets):
            row_str.append(f"{cov_matrix[i][j]:.6f}")
        print(" ".join(row_str))

if __name__ == "__main__":
    main()