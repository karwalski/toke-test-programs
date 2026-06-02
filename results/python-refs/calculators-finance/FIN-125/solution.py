import sys
from datetime import datetime

def main():
    positions = []
    
    # Read input from stdin
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
            
        parts = line.split()
        ticker = parts[0]
        buy_date = parts[1]
        buy_price = float(parts[2])
        current_price = float(parts[3])
        qty = int(parts[4])
        
        # Calculate unrealized loss (only if current_price < buy_price)
        if current_price < buy_price:
            loss_per_share = current_price - buy_price
            total_loss = loss_per_share * qty
            positions.append((ticker, total_loss))
    
    # Sort by loss size (most negative first, which means largest loss first)
    positions.sort(key=lambda x: x[1])
    
    # Output harvestable losses
    for ticker, loss in positions:
        print(f"{ticker} {loss:.2f}")

if __name__ == "__main__":
    main()