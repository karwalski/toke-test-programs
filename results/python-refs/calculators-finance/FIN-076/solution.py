import sys

total_weighted_score = 0
total_weight = 0

for line in sys.stdin:
    line = line.strip()
    if line:
        parts = line.split()
        factor_name = parts[0]
        score = float(parts[1])
        weight = float(parts[2])
        
        total_weighted_score += score * weight
        total_weight += weight

composite_score = total_weighted_score / total_weight

# Determine risk category
if composite_score < 30:
    category = "LOW"
elif composite_score < 70:
    category = "MEDIUM"
else:
    category = "HIGH"

print(f"{composite_score:.1f}")
print(category)