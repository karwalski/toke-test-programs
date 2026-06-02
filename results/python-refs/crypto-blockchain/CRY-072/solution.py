import json
import sys

# Read gas limit
gas_limit = int(input().strip())

# Read gas cost table
gas_costs = json.loads(input().strip())

# Read operations and calculate total gas
total_gas = 0
operation_count = 0

try:
    while True:
        line = input().strip()
        if line:
            operation_count += 1
            operation_gas = gas_costs[line]
            total_gas += operation_gas
            
            if total_gas > gas_limit:
                print(total_gas)
                print(f"OUT_OF_GAS at operation {operation_count}")
                sys.exit()
except EOFError:
    pass

print(total_gas)
print("SUCCESS")