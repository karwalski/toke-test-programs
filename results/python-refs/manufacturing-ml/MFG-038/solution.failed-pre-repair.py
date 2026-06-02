import sys
import csv
import json

# Read CSV data from stdin
reader = csv.DictReader(sys.stdin)
categories = []
total_scrap = 0
total_produced = 0

for row in reader:
    category = row['category']
    scrap_count = int(row['scrap_count'])
    total_produced_cat = int(row['total_produced'])
    
    rate = scrap_count / total_produced_cat
    categories.append({
        'category': category,
        'rate': rate
    })
    
    total_scrap += scrap_count
    total_produced += total_produced_cat

# Sort categories by rate (descending), then by category name for ties
categories.sort(key=lambda x: (-x['rate'], x['category']))

# Calculate overall rate
overall_rate = total_scrap / total_produced

# Create output
result = {
    'overall_rate': overall_rate,
    'categories': categories
}

# Output JSON
print(json.dumps(result, separators=(',', ':')))