import sys
import csv
import json

reader = csv.DictReader(sys.stdin)
categories = []
total_scrap = 0
total_produced = 0

for row in reader:
    category = row['category']
    scrap_count = int(row['scrap_count'])
    total_produced_cat = int(row['total_produced'])
    
    rate = round(scrap_count / total_produced_cat, 2)
    categories.append({
        'category': category,
        'rate': rate
    })
    
    total_scrap += scrap_count
    total_produced += total_produced_cat

categories.sort(key=lambda x: -x['rate'])

overall_rate = round(total_scrap / total_produced, 2)

result = {
    'overall_rate': overall_rate,
    'categories': categories
}

print(json.dumps(result, separators=(',', ':')))