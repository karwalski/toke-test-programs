import json
import sys

# Read initial balances
initial_line = input().strip()
balances = json.loads(initial_line)
allowances = {}

# Process commands
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    parts = line.split()
    command = parts[0]
    
    if command == "APPROVE":
        owner = parts[1]
        spender = parts[2]
        amount = int(parts[3])
        
        if owner not in allowances:
            allowances[owner] = {}
        allowances[owner][spender] = amount
    
    elif command == "TRANSFER_FROM":
        spender = parts[1]
        owner = parts[2]
        to = parts[3]
        amount = int(parts[4])
        
        # Check if allowance exists and is sufficient
        if owner in allowances and spender in allowances[owner]:
            if allowances[owner][spender] >= amount and balances[owner] >= amount:
                # Transfer tokens
                balances[owner] -= amount
                balances[to] += amount
                
                # Reduce allowance
                allowances[owner][spender] -= amount

# Output result
result = {
    "balances": balances,
    "allowances": allowances
}

print(json.dumps(result, separators=(',', ':')))