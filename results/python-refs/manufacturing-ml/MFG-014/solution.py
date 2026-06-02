import csv
import json
import sys

# Read CSV from stdin
reader = csv.DictReader(sys.stdin)
data = []

for row in reader:
    data.append({
        'defect_type': row['defect_type'],
        'count': int(row['count'])
    })

# Sort by count descending
data.sort(key=lambda x: x['count'], reverse=True)

# Calculate total count
total_count = sum(item['count'] for item in data)

# Calculate cumulative percentages
cumulative_count = 0
result = []

for item in data:
    cumulative_count += item['count']
    cumulative_percent = (cumulative_count / total_count) * 100
    
    result.append({
        'defect_type': item['defect_type'],
        'count': item['count'],
        'cumulative_percent': cumulative_percent
    })

# Output as JSON
print(json.dumps(result, separators=(',', ':')))