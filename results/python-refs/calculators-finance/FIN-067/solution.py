import sys

assets = []
volatilities = []

for line in sys.stdin:
    line = line.strip()
    if line:
        parts = line.split()
        asset = parts[0]
        vol = float(parts[1])
        assets.append(asset)
        volatilities.append(vol)

# Calculate inverse volatilities
inverse_vols = [1/vol for vol in volatilities]

# Calculate sum of inverse volatilities
sum_inverse = sum(inverse_vols)

# Calculate weights (normalized)
weights = [inv_vol / sum_inverse for inv_vol in inverse_vols]

# Output
for i, asset in enumerate(assets):
    weight_pct = weights[i] * 100
    print(f"{asset} {weight_pct:.2f}%")