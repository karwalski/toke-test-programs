import sys
from collections import defaultdict

def main():
    # Read all input
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    # Parse exchange rates
    rates = defaultdict(dict)
    
    for line in lines:
        if line.startswith('CHECK'):
            parts = line.split()
            cur1, cur2, cur3 = parts[1], parts[2], parts[3]
            break
        else:
            parts = line.split()
            from_cur, to_cur, rate = parts[0], parts[1], float(parts[2])
            rates[from_cur][to_cur] = rate
            # Add reverse rate
            rates[to_cur][from_cur] = 1.0 / rate
    
    # Check triangular arbitrage: CUR1 -> CUR2 -> CUR3 -> CUR1
    try:
        # Path: cur1 -> cur2 -> cur3 -> cur1
        rate1 = rates[cur1][cur2]  # cur1 to cur2
        rate2 = rates[cur2][cur3]  # cur2 to cur3
        rate3 = rates[cur3][cur1]  # cur3 to cur1
        
        final_amount = rate1 * rate2 * rate3
        
        if final_amount > 1.0:
            profit_percent = (final_amount - 1.0) * 100
            print(f"ARBITRAGE {profit_percent:.2f}%")
        else:
            print("NO_ARBITRAGE")
    except KeyError:
        print("NO_ARBITRAGE")

if __name__ == "__main__":
    main()