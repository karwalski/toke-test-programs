# Read input from stdin
line = input().strip()
gross_annual, tax_rate, super_rate, medicare_rate = line.split()

# Convert to appropriate types
gross_annual = float(gross_annual)
tax_rate = float(tax_rate)
super_rate = float(super_rate)
medicare_rate = float(medicare_rate)

# Calculate annual tax (tax rate + medicare levy applied to gross)
annual_tax = gross_annual * (tax_rate + medicare_rate)

# Calculate annual superannuation (super rate applied to gross)
annual_super = gross_annual * super_rate

# Calculate annual net pay (gross - tax - super)
annual_net = gross_annual - annual_tax - annual_super

# Output results with 2 decimal places
print(f"{annual_tax:.2f}")
print(f"{annual_super:.2f}")
print(f"{annual_net:.2f}")