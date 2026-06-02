import sys

# Read total value
total_value = float(input().strip())

# Read asset data
assets = []
while True:
    try:
        line = input().strip()
        if not line:
            break
        parts = line.split()
        asset_name = parts[0]
        current_pct = float(parts[1])
        target_pct = float(parts[2])
        assets.append((asset_name, current_pct, target_pct))
    except EOFError:
        break

# Calculate rebalancing for each asset
for asset_name, current_pct, target_pct in assets:
    current_value = total_value * current_pct / 100
    target_value = total_value * target_pct / 100
    difference = target_value - current_value
    
    if difference > 0.01:  # Need to buy (accounting for small floating point differences)
        print(f"{asset_name} BUY {difference:.2f}")
    elif difference < -0.01:  # Need to sell
        print(f"{asset_name} SELL {abs(difference):.2f}")
    else:  # Hold (difference is essentially zero)
        print(f"{asset_name} HOLD 0.00")