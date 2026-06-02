import sys
from collections import defaultdict

def main():
    balances = defaultdict(int)
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
            
        parts = line.split()
        if len(parts) != 4:
            continue
            
        date, debit_account, credit_account, amount = parts
        amount = int(amount)
        
        # Debit increases the account (positive)
        balances[debit_account] += amount
        # Credit decreases the account (negative)
        balances[credit_account] -= amount
    
    # Sort accounts alphabetically and output
    for account in sorted(balances.keys()):
        balance = balances[account]
        if balance > 0:
            print(f"{account} {balance} DR")
        else:
            print(f"{account} {-balance} CR")

if __name__ == "__main__":
    main()