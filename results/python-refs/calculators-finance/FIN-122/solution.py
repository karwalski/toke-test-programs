import sys

def calculate_profit_loss():
    holdings = []  # List of (quantity, price) tuples for FIFO
    total_profit_loss = 0.0
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
            
        parts = line.split()
        action = parts[0]
        qty = float(parts[1])
        price = float(parts[2])
        
        if action == "BUY":
            holdings.append((qty, price))
        elif action == "SELL":
            remaining_to_sell = qty
            
            while remaining_to_sell > 0 and holdings:
                held_qty, held_price = holdings[0]
                
                if held_qty <= remaining_to_sell:
                    # Sell entire holding
                    profit_loss = held_qty * (price - held_price)
                    total_profit_loss += profit_loss
                    remaining_to_sell -= held_qty
                    holdings.pop(0)
                else:
                    # Partially sell holding
                    profit_loss = remaining_to_sell * (price - held_price)
                    total_profit_loss += profit_loss
                    holdings[0] = (held_qty - remaining_to_sell, held_price)
                    remaining_to_sell = 0
    
    print(f"{total_profit_loss:.2f}")

calculate_profit_loss()