damage, deductible, coverage_limit, copay_pct = map(float, input().split())

# Amount after deductible
amount_after_deductible = max(0, damage - deductible)

# Apply coverage limit
covered_amount = min(amount_after_deductible, coverage_limit)

# Calculate copay
claimant_copay = covered_amount * copay_pct
insurer_pays = covered_amount - claimant_copay

# Total claimant pays is deductible plus copay
claimant_pays = deductible + claimant_copay

print(f"{claimant_pays:.2f}")
print(f"{insurer_pays:.2f}")