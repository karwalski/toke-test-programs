import json
import sys

# Read initial state
initial_state = json.loads(input().strip())
collateral = initial_state["collateral"]
wrapped_supply = initial_state["wrapped_supply"]
rate = initial_state["rate"]

# Process commands
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    parts = line.split()
    command = parts[0]
    
    if command == "MINT":
        amount = int(parts[1])
        if amount > 0:
            collateral += amount
            wrapped_supply += amount
            print("OK")
        else:
            print("ERROR")
    
    elif command == "BURN":
        amount = int(parts[1])
        if amount > 0 and amount <= wrapped_supply:
            collateral -= amount
            wrapped_supply -= amount
            print("OK")
        else:
            print("ERROR")
    
    elif command == "STATUS":
        if wrapped_supply == 0:
            ratio = 0.0
        else:
            ratio = collateral / wrapped_supply
        print(f"collateral={collateral} wrapped={wrapped_supply} ratio={ratio:.2f}")