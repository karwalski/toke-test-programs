import sys
import json

def main():
    buy_orders = []  # List of (amount, price)
    sell_orders = []  # List of (amount, price)
    executed_trades = []
    
    # Read all input
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
            
        parts = line.split()
        if len(parts) != 3:
            continue
            
        command = parts[0]
        amount = int(parts[1])
        price = int(parts[2])
        
        if command == "BUY":
            # Try to match with existing sell orders
            remaining_amount = amount
            
            # Sort sell orders by price (ascending) for best match
            sell_orders.sort(key=lambda x: x[1])
            
            i = 0
            while i < len(sell_orders) and remaining_amount > 0:
                sell_amount, sell_price = sell_orders[i]
                
                # Can only match if buy price >= sell price
                if price >= sell_price:
                    trade_amount = min(remaining_amount, sell_amount)
                    
                    # Execute trade at sell price
                    executed_trades.append({
                        "price": sell_price,
                        "amount": trade_amount
                    })
                    
                    remaining_amount -= trade_amount
                    
                    # Update or remove sell order
                    if sell_amount > trade_amount:
                        sell_orders[i] = (sell_amount - trade_amount, sell_price)
                        i += 1
                    else:
                        sell_orders.pop(i)
                else:
                    i += 1
            
            # Add remaining buy amount as new order
            if remaining_amount > 0:
                buy_orders.append((remaining_amount, price))
                
        elif command == "SELL":
            # Try to match with existing buy orders
            remaining_amount = amount
            
            # Sort buy orders by price (descending) for best match
            buy_orders.sort(key=lambda x: x[1], reverse=True)
            
            i = 0
            while i < len(buy_orders) and remaining_amount > 0:
                buy_amount, buy_price = buy_orders[i]
                
                # Can only match if buy price >= sell price
                if buy_price >= price:
                    trade_amount = min(remaining_amount, buy_amount)
                    
                    # Execute trade at buy price
                    executed_trades.append({
                        "price": buy_price,
                        "amount": trade_amount
                    })
                    
                    remaining_amount -= trade_amount
                    
                    # Update or remove buy order
                    if buy_amount > trade_amount:
                        buy_orders[i] = (buy_amount - trade_amount, buy_price)
                        i += 1
                    else:
                        buy_orders.pop(i)
                else:
                    i += 1
            
            # Add remaining sell amount as new order
            if remaining_amount > 0:
                sell_orders.append((remaining_amount, price))
    
    # Output executed trades
    print(json.dumps(executed_trades, separators=(',', ':')))
    
    # Format remaining orders
    remaining = {
        "sells": [{"amount": amount, "price": price} for amount, price in sell_orders],
        "buys": [{"amount": amount, "price": price} for amount, price in buy_orders]
    }
    
    print(json.dumps(remaining, separators=(',', ':')))

if __name__ == "__main__":
    main()