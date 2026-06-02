import csv
import json
import sys

# Read CSV from stdin
reader = csv.DictReader(sys.stdin)
items = []

for row in reader:
    item = row['item']
    daily_demand = int(row['daily_demand'])
    lead_days = int(row['lead_days'])
    safety_stock_days = int(row['safety_stock_days'])
    
    # Calculate reorder point: (lead time + safety stock days) * daily demand
    reorder_point = (lead_days + safety_stock_days) * daily_demand
    
    items.append({
        "item": item,
        "reorder_point": reorder_point
    })

# Output JSON to stdout
output = {"items": items}
print(json.dumps(output, separators=(',', ':')))