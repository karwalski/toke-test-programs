import sys

# Read input
line = input().strip()
cost, salvage, useful_life = map(int, line.split())

# Calculate sum of years
sum_of_years = useful_life * (useful_life + 1) // 2

# Calculate depreciation for each year
depreciable_amount = cost - salvage
book_value = cost

for year in range(1, useful_life + 1):
    # Calculate depreciation for this year
    depreciation = (useful_life - year + 1) / sum_of_years * depreciable_amount
    book_value -= depreciation
    
    # Output in required format
    print(f"{year},{depreciation:.2f},{book_value:.2f}")