import sys
import csv
import json

# Read CSV from stdin
csv_reader = csv.DictReader(sys.stdin)
suppliers = []

for row in csv_reader:
    supplier = row['supplier']
    lots_received = int(row['lots_received'])
    lots_rejected = int(row['lots_rejected'])
    on_time_deliveries = int(row['on_time_deliveries'])
    total_deliveries = int(row['total_deliveries'])
    
    # Calculate quality percentage (lots not rejected / total lots)
    quality_pct = ((lots_received - lots_rejected) / lots_received) * 100
    
    # Calculate delivery percentage (on time / total deliveries)
    delivery_pct = (on_time_deliveries / total_deliveries) * 100
    
    # Calculate composite score (average of quality and delivery percentages)
    composite = (quality_pct + delivery_pct) / 2
    
    suppliers.append({
        'supplier': supplier,
        'quality_pct': quality_pct,
        'delivery_pct': delivery_pct,
        'composite': composite
    })

# Sort by composite score descending
suppliers.sort(key=lambda x: x['composite'], reverse=True)

# Output JSON
result = {'suppliers': suppliers}
print(json.dumps(result, separators=(',', ':')))