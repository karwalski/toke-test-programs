import sys

total_income = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    parts = line.split()
    ticker = parts[0]
    shares = int(parts[1])
    price = float(parts[2])
    annual_dividend = float(parts[3])
    
    # Calculate dividend yield as percentage
    yield_percent = (annual_dividend / price) * 100
    
    # Calculate annual income
    annual_income = shares * annual_dividend
    total_income += annual_income
    
    # Print formatted output
    print(f"{ticker} {yield_percent:.2f}% {annual_income:.2f}")

print(f"TOTAL {total_income:.2f}")