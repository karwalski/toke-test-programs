import sys

# Read initial reserves
line = input().strip()
reserve_x, reserve_y = map(int, line.split())

# Calculate initial constant k
k = reserve_x * reserve_y

# Process swap commands
for line in sys.stdin:
    line = line.strip()
    if not line:
        break
    
    parts = line.split()
    command = parts[0]
    amount = int(parts[1])
    
    if command == "SWAP_X":
        # Adding amount to reserve_x, calculate how much reserve_y to give
        new_reserve_x = reserve_x + amount
        new_reserve_y = k // new_reserve_x
        amount_received = reserve_y - new_reserve_y
        
        reserve_x = new_reserve_x
        reserve_y = new_reserve_y
        
        print(amount_received)
        
    elif command == "SWAP_Y":
        # Adding amount to reserve_y, calculate how much reserve_x to give
        new_reserve_y = reserve_y + amount
        new_reserve_x = k // new_reserve_y
        amount_received = reserve_x - new_reserve_x
        
        reserve_x = new_reserve_x
        reserve_y = new_reserve_y
        
        print(amount_received)

print(f"RESERVES {reserve_x} {reserve_y}")